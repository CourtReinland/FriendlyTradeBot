"""
Real Data Arena — Full Evolutionary Run on Historical Market Data

Run with rich CLI configuration + persistence:

    uv run python scripts/run_real_data_arena.py --gens 18 --pop 12 \
        --creative 0.18 --allocator regime_aware --save runs/my_run/

This script runs the complete Multi-Agent Arena on actual historical prices
(SPY, TLT, IEI, GLD, DBC, etc.) from ~2004 to present.

It demonstrates:
- Diverse strategy population (Dalio, Momentum, MeanReversion, Defensive, etc.)
- Ensemble-aware scoring via MultiAgentRunner + MetaAllocator
- Evolutionary loop with mutation + Grok creative mutation
- Full configurability via Typer CLI (no extra subcommand needed)
- Optional JSON persistence for populations between runs
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))   # allow "from demo_agents import ..." when running the script

import typer
from typing import Optional
from pathlib import Path

import numpy as np
import polars as pl

from friendly_trade_bot.agents.dalio_allweather import DalioAllWeatherAgent
from friendly_trade_bot.arena import (
    ArenaConfig,
    EnsembleScorer,
    MultiAgentRunner,
    MutationOperator,
    Population,
    SimpleArena,
    create_default_meta_allocator,
    FitnessWeightedAllocator,
    EqualWeightAllocator,
    RegimeAwareAllocator,
)
from friendly_trade_bot.arena.population import AgentGenome
from friendly_trade_bot.backtest.engine import BacktestConfig, BacktestEngine
from friendly_trade_bot.data.download import DownloadConfig, download_universe, CORE_UNIVERSE


def load_or_download_real_data(start_date: str = "2004-11-01") -> pl.DataFrame:
    """Load real ETF data. Downloads if not present."""
    data_dir = Path("data/raw")
    data_dir.mkdir(parents=True, exist_ok=True)

    required = ["SPY", "TLT", "IEI", "GLD", "DBC"]

    # Download if missing
    missing = [t for t in required if not (data_dir / f"{t}.parquet").exists()]
    if missing:
        print(f"Downloading real data for: {missing}")
        cfg = DownloadConfig(
            tickers=missing,
            start=start_date,
            output_dir=data_dir,
            overwrite=False,
        )
        download_universe(cfg)
        print("Download complete.\n")

    # Load and combine
    dfs = []
    for ticker in required:
        path = data_dir / f"{ticker}.parquet"
        if path.exists():
            df = pl.read_parquet(path).select(["date", "close"])
            dfs.append(df.with_columns(pl.lit(ticker).alias("ticker")))

    if not dfs:
        raise FileNotFoundError("No real data found. Check data/raw/")

    combined = pl.concat(dfs).sort(["date", "ticker"]).drop_nulls(subset=["close"])
    combined = combined.unique(subset=["date", "ticker"]).sort(["date", "ticker"])

    print(f"Loaded real data: {combined['date'].min()} → {combined['date'].max()}")
    print(f"Tickers: {required}\n")
    return combined


def create_diverse_real_data_population(size: int = 10) -> Population:
    """Create a population with meaningfully different strategies."""
    pop = Population(name="RealDataArena_v1")

    # 1. Classic Dalio All-Weather
    dalio = DalioAllWeatherAgent(target_vol=0.08, equity_reduction_in_stress=0.40)
    dalio_genome = AgentGenome("DalioAllWeather", {"target_vol": 0.08, "equity_reduction_in_stress": 0.40})
    pop.add_agent(dalio, dalio_genome, "dalio_base")

    # 2–4. Different Dalio parameter sets
    for i, (tv, reduction) in enumerate([
        (0.06, 0.35),
        (0.10, 0.50),
        (0.07, 0.45),
    ]):
        agent = DalioAllWeatherAgent(target_vol=tv, equity_reduction_in_stress=reduction)
        genome = AgentGenome("DalioAllWeather", {"target_vol": tv, "equity_reduction_in_stress": reduction})
        pop.add_agent(agent, genome, f"dalio_var_{i}")

    # 5. Momentum style (lightweight)
    from friendly_trade_bot.agents import SimpleMomentumAgent
    mom = SimpleMomentumAgent(lookback=25, target_vol=0.09)
    mom_genome = AgentGenome("SimpleMomentum", {"lookback": 25, "target_vol": 0.09})
    pop.add_agent(mom, mom_genome, "momentum_1")

    # 6. Defensive
    from friendly_trade_bot.agents import DefensiveAgent
    defensive = DefensiveAgent()
    def_genome = AgentGenome("Defensive", {})
    pop.add_agent(defensive, def_genome, "defensive_1")

    # 7. Mean Reversion
    from friendly_trade_bot.agents import MeanReversionAgent
    mr = MeanReversionAgent(lookback=12)
    mr_genome = AgentGenome("MeanReversion", {"lookback": 12})
    pop.add_agent(mr, mr_genome, "meanrev_1")

    # Fill remaining slots with variations
    while len(pop) < size:
        idx = len(pop) % 4
        if idx == 0:
            agent = DalioAllWeatherAgent(target_vol=0.075, equity_reduction_in_stress=0.42)
            genome = AgentGenome("DalioAllWeather", {"target_vol": 0.075, "equity_reduction_in_stress": 0.42})
        elif idx == 1:
            agent = SimpleMomentumAgent(lookback=30, target_vol=0.08)
            genome = AgentGenome("SimpleMomentum", {"lookback": 30, "target_vol": 0.08})
        elif idx == 2:
            agent = DefensiveAgent()
            genome = AgentGenome("Defensive", {})
        else:
            agent = MeanReversionAgent(lookback=8)
            genome = AgentGenome("MeanReversion", {"lookback": 8})

        pop.add_agent(agent, genome, f"var_{len(pop)}")

    return pop


def run(
    generations: int = typer.Option(18, "--gens", "-g", help="Number of evolutionary generations"),
    population_size: int = typer.Option(12, "--pop", "-p", help="Population size"),
    keep_top: int = typer.Option(6, "--keep", "-k", help="Number of top agents kept each generation"),
    mutation_rate: float = typer.Option(0.60, "--mut-rate", help="Base mutation probability"),
    creative_rate: float = typer.Option(0.15, "--creative", "-c", help="Base creative mutation rate"),
    exploration_bonus: float = typer.Option(0.08, "--bonus", help="Fitness bonus for creative mutants"),
    adaptive: bool = typer.Option(True, "--adaptive/--no-adaptive", help="Use adaptive creative rate controller"),
    meta_allocator: str = typer.Option(
        "fitness_weighted",
        "--allocator",
        "-a",
        help="Meta allocator: fitness_weighted | equal | regime_aware",
    ),
    save_path: Optional[str] = typer.Option(
        None, "--save", "-s", help="Directory or file path to save population snapshots (JSON)"
    ),
    seed: Optional[int] = typer.Option(None, "--seed", help="Optional RNG seed for reproducibility"),
):
    """Run the full evolutionary arena on real historical ETF data with rich configuration."""
    print("=" * 72)
    print("FriendlyTradeBot — Real Historical Data Arena (configurable)")
    print("=" * 72 + "\n")

    # Resolve allocator
    alloc_map = {
        "equal": EqualWeightAllocator(),
        "fitness_weighted": create_default_meta_allocator(),
        "regime_aware": RegimeAwareAllocator(),
    }
    chosen_allocator = alloc_map.get(meta_allocator.lower(), create_default_meta_allocator())
    print(f"Using meta-allocator: {meta_allocator}")

    # Load real market data
    price_data = load_or_download_real_data(start_date="2004-11-01")

    # Engine (conservative real-data settings)
    engine = BacktestEngine(
        config=BacktestConfig(
            initial_capital=10_000,
            rebalance_frequency="weekly",
            target_portfolio_vol=0.08,
            max_weight_per_asset=0.35,
        )
    )

    # Scoring
    runner = MultiAgentRunner(engine, meta_allocator=chosen_allocator)
    scorer = EnsembleScorer(engine)
    scorer.runner = runner

    # Mutation operator
    mutator = MutationOperator()

    # Initial diverse population
    print("Creating diverse initial population...")
    initial_pop = create_diverse_real_data_population(size=population_size)
    print(f"Initial population size: {len(initial_pop)}\n")

    # Build rich ArenaConfig
    cfg = ArenaConfig(
        population_size=population_size,
        keep_top_n=keep_top,
        generations=generations,
        mutation_rate=mutation_rate,
        creative_mutation_rate=creative_rate,
        creative_fitness_boost=exploration_bonus,
        exploration_bonus=exploration_bonus,
        use_adaptive_creative_rate=adaptive,
        track_history=True,
        meta_allocator_type=meta_allocator,
        persistence_path=save_path,
        save_every_n_generations=1 if save_path else 0,
        seed=seed,
    )

    # Arena
    arena = SimpleArena(
        engine=engine,
        scorer=scorer,
        mutator=mutator,
        config=cfg,
        meta_allocator=chosen_allocator,
    )

    # Optional: wire persistence callback into arena history tracking
    original_run_gen = arena.run_generation

    def run_gen_with_persist(population, price_data, regimes=None):
        new_pop = original_run_gen(population, price_data, regimes)
        if cfg.persistence_path:
            out_path = Path(cfg.persistence_path)
            if out_path.is_dir() or str(out_path).endswith("/"):
                out_path = out_path / f"population_gen{new_pop.generation}.json"
            new_pop.save(out_path)
        return new_pop

    arena.run_generation = run_gen_with_persist

    print(f"Starting real-data evolutionary run ({generations} gens, pop={population_size}, allocator={meta_allocator})...\n")
    final_population = arena.run(initial_pop, price_data)

    # Final persistence snapshot
    if save_path:
        final_path = Path(save_path)
        if final_path.is_dir() or str(final_path).endswith("/"):
            final_path = final_path / f"population_final_gen{final_population.generation}.json"
        final_population.save(final_path)

    print("\n" + "=" * 72)
    print("REAL DATA ARENA RUN COMPLETE")
    print("=" * 72)
    print(f"Final generation: {final_population.generation}")
    print(f"Final population size: {len(final_population)}")
    print(f"Best fitness: {max((m.fitness or 0.0) for m in final_population.members.values()):.4f}")


if __name__ == "__main__":
    typer.run(run)