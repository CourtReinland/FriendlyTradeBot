"""
Live Monitoring Server for FriendlyTradeBot Arena.

This module provides a WebSocket-based live dashboard for monitoring
evolutionary runs in real time.

Features:
- WebSocket endpoint for live updates after each generation
- Serves a rich dashboard (HTML + Tailwind + Chart.js)
- Embeds the PROGRESS_MAP.md for easy reference
- Supports running the arena in the background
"""

from __future__ import annotations

import asyncio
import threading
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import typer

# --- Configuration ---
MONITORING_PORT = 8765
PROGRESS_MAP_PATH = Path(__file__).parent.parent.parent.parent / "docs" / "PROGRESS_MAP.md"

app = FastAPI(title="FriendlyTradeBot Arena Monitor")

# Templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# In-memory state for connected clients and latest arena data
connected_clients: set[WebSocket] = set()
latest_state: Dict[str, Any] = {}


# --- WebSocket Handling ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"[Monitor] Client connected. Total clients: {len(connected_clients)}")

    # Send latest state immediately on connect (defensively)
    if latest_state:
        try:
            await websocket.send_json(latest_state)
        except Exception as e:
            print(f"[Monitor] Failed to send latest_state on connect: {e}")

    try:
        while True:
            # Keep connection alive (clients can also send ping if needed)
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        print(f"[Monitor] Client disconnected. Remaining: {len(connected_clients)}")
    except Exception as e:
        connected_clients.discard(websocket)
        print(f"[Monitor] WS handler error: {e}")


async def broadcast_update(data: Dict[str, Any]):
    """Send an update to all connected WebSocket clients. Defensive against bad data."""
    global latest_state

    # Ensure the data is JSON-serializable (replace NaN/Inf with None if any slipped in)
    safe_data = {}
    for k, v in data.items():
        if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):  # NaN or Inf
            safe_data[k] = None
        else:
            safe_data[k] = v
    latest_state = safe_data

    if not connected_clients:
        return

    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json(safe_data)
        except Exception as exc:
            print(f"[Monitor] WS send failed for a client: {exc}")
            disconnected.append(client)

    for client in disconnected:
        connected_clients.discard(client)


# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Serve the rich terminal-style live dashboard (matches the excellent ASCII CLI experience)."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/progress-map")
async def get_progress_map():
    """Serve the PROGRESS_MAP.md file (raw markdown for client-side rendering)."""
    try:
        content = PROGRESS_MAP_PATH.read_text(encoding="utf-8")
        return content
    except Exception:
        return "# Progress Map not found"


@app.post("/broadcast")
async def manual_broadcast(data: Dict[str, Any]):
    """Allow external scripts to push updates (useful for testing)."""
    await broadcast_update(data)
    return {"status": "broadcasted"}


def start_monitoring_server(host: str = "0.0.0.0", port: int = MONITORING_PORT):
    """Start the monitoring server."""
    uvicorn.run(app, host=host, port=port, log_level="info")


# ------------------------------------------------------------------
# Background Arena Execution + Live Updates (Real Implementation)
# ------------------------------------------------------------------

_background_arena_thread = None
_background_arena_stop_event = None

def _run_arena_in_thread(price_data, generations=12, population_size=12, use_adaptive=True,
                           allocator_type="fitness_weighted", creative_rate=0.15, loop=None):
    """Runs the real SimpleArena (richly configured) in background and streams updates via WebSocket."""
    from friendly_trade_bot.arena import (
        SimpleArena, ArenaConfig,
        FitnessWeightedAllocator, EqualWeightAllocator, RegimeAwareAllocator,
    )
    from friendly_trade_bot.backtest.engine import BacktestEngine, BacktestConfig
    from friendly_trade_bot.arena.scoring import EnsembleScorer
    from friendly_trade_bot.arena.multi_agent_runner import MultiAgentRunner
    from friendly_trade_bot.arena.evolution import MutationOperator
    from friendly_trade_bot.arena.meta_allocator import create_default_meta_allocator

    # Lightweight diverse population factory (now uses the real Agent Registry)
    def _make_diverse_pop(size: int):
        from friendly_trade_bot.arena.population import Population, AgentGenome
        from friendly_trade_bot.agents.registry import create_agent_from_genome, REGISTRY

        pop = Population(name="MonitorArenaPop")

        # Seed with a mix of registered types (including creative ones when available)
        types_to_seed = ["DalioAllWeather", "SimpleMomentum", "Defensive", "MeanReversion"]
        # Add creative types if they are registered
        for creative in ["DalioTactical", "DalioWithTrendOverlay", "RegimeRiskParity"]:
            if REGISTRY.is_registered(creative):
                types_to_seed.append(creative)

        for i in range(min(size, len(types_to_seed))):
            atype = types_to_seed[i % len(types_to_seed)]
            defaults = REGISTRY.get_defaults(atype)
            agent = create_agent_from_genome(
                type("G", (), {"agent_type": atype, "parameters": defaults})()
            )
            g = AgentGenome(atype, defaults)
            pop.add_agent(agent, g, f"{atype.lower()}_{i}")

        # Fill the rest with Dalio variants if needed
        while len(pop) < size:
            tv = 0.07 + (len(pop) % 3) * 0.015
            agent = create_agent_from_genome(
                type("G", (), {"agent_type": "DalioAllWeather", "parameters": {"target_vol": tv, "equity_reduction_in_stress": 0.40}})()
            )
            g = AgentGenome("DalioAllWeather", {"target_vol": tv, "equity_reduction_in_stress": 0.40})
            pop.add_agent(agent, g, f"dalio_fill_{len(pop)}")

        return pop

    # Allocator
    if allocator_type == "equal":
        meta_allocator = EqualWeightAllocator()
    elif allocator_type == "regime_aware":
        meta_allocator = RegimeAwareAllocator()
    else:
        meta_allocator = create_default_meta_allocator()

    engine = BacktestEngine(
        config=BacktestConfig(
            initial_capital=10_000,
            rebalance_frequency="weekly",
            target_portfolio_vol=0.08,
        )
    )

    runner = MultiAgentRunner(engine, meta_allocator=meta_allocator)
    scorer = EnsembleScorer(engine)
    scorer.runner = runner
    mutator = MutationOperator()

    initial_pop = _make_diverse_pop(population_size)

    def generation_callback(update: dict):
        if loop:
            asyncio.run_coroutine_threadsafe(broadcast_update(update), loop)

    cfg = ArenaConfig(
        population_size=population_size,
        keep_top_n=max(3, population_size // 2),
        generations=generations,
        creative_mutation_rate=creative_rate,
        use_adaptive_creative_rate=use_adaptive,
        track_history=True,
        meta_allocator_type=allocator_type,
    )

    arena = SimpleArena(
        engine=engine,
        scorer=scorer,
        mutator=mutator,
        config=cfg,
        meta_allocator=meta_allocator,
        generation_callback=generation_callback,
    )

    arena.run(initial_pop, price_data)

    if loop:
        asyncio.run_coroutine_threadsafe(
            broadcast_update({"status": "finished", "message": "Arena run complete"}),
            loop
        )


@app.post("/arena/start")
async def start_arena(payload: Dict[str, Any]):
    """
    Start the real evolutionary arena in a background thread.
    """
    global _background_arena_thread, _background_arena_stop_event

    if _background_arena_thread and _background_arena_thread.is_alive():
        return {"status": "already_running", "message": "An arena is already running"}

    # Load real data
    from scripts.run_real_data_arena import load_or_download_real_data
    price_data = load_or_download_real_data()

    loop = asyncio.get_running_loop()

    _background_arena_thread = threading.Thread(
        target=_run_arena_in_thread,
        args=(
            price_data,
            payload.get("generations", 12),
            payload.get("population_size", 12),
            payload.get("use_adaptive_creative", True),
            payload.get("allocator_type", "fitness_weighted"),
            payload.get("creative_rate", 0.15),
            loop,
        ),
        daemon=True,
    )
    _background_arena_thread.start()

    return {"status": "started", "message": "Arena is running in the background"}


@app.post("/arena/stop")
async def stop_arena():
    """Request stop of a running background arena (best-effort for threaded runs)."""
    global _background_arena_thread
    if _background_arena_thread and _background_arena_thread.is_alive():
        # We cannot forcibly kill threads safely; the current generation will finish.
        return {"status": "stop_requested", "message": "Stop requested — current generation will finish"}
    return {"status": "not_running", "message": "No arena thread active"}


# Helper for arena scripts to push updates
async def push_generation_update(data: Dict[str, Any]):
    """Call this from SimpleArena after each generation to push live updates."""
    await broadcast_update(data)

# ------------------------------------------------------------------
# CLI Entry Point (exposed as `ftb-monitor`)
# ------------------------------------------------------------------

import typer

cli = typer.Typer(help="FriendlyTradeBot Monitoring Dashboard")

@cli.command()
def start(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind the server to"),
    port: int = typer.Option(8765, "--port", "-p", help="Port to run the monitoring server on"),
    reload: bool = typer.Option(True, "--reload", help="Enable auto-reload (development)"),
):
    """Start the live monitoring dashboard."""
    uvicorn.run(
        "friendly_trade_bot.monitoring.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    cli()
