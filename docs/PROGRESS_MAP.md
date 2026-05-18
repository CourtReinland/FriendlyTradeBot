# FriendlyTradeBot – Progress & Architecture Map

**Last Updated:** 2026-05-18 (late)  
**Current Focus:** Core Evolutionary Power – Agent Factory complete + starting Regime Awareness

**Latest Milestone (just completed):**  
Full Agent Factory + Registry implemented. Creative mutations now intelligently propose and instantiate real, behaviorally distinct agents (DalioTactical, DalioWithTrendOverlay, RegimeRiskParity, etc.). The evolutionary loop finally delivers on "new species" instead of just parameter tweaks.

---

## High-Level Architecture (ASCII View)

```
┌────────────────────────────────────────────────────────────────────┐
│                    FRIENDLY TRADE BOT SYSTEM                       │
└────────────────────────────────────────────────────────────────────┘

Layer 0: Foundations
  ├── Repository + Git + pyproject.toml
  └── PROGRESS_MAP.md (this file)

Layer 1: Data & Simulation
  ├── Real ETF Data Downloader                    [DONE]
  └── Synthetic Regime Generator (with stress)    [DONE]

Layer 2: Backtesting Engine
  ├── Event-driven + realistic costs
  ├── Correlation-aware volatility targeting
  ├── Full covariance matrix exposure
  └── MetaAllocator integration                   [DONE]

Layer 3: Agents
  ├── Base Agent Protocol + WorldState
  └── Multiple strategy types (Dalio, Momentum, MeanReversion, Defensive, etc.)   [DONE]

Layer 4: Validation Harness                        [VERY STRONG]
  ├── Purged Walk-Forward
  ├── Monte Carlo (Block Bootstrap + Adaptive)
  ├── Stress Testing + Recovery Analysis
  └── Unified ValidationReport

Layer 5: Multi-Agent Arena (Phase 2) ← CURRENT WORK
  ├── Population + Genomes
  ├── MultiAgentRunner (Leave-One-Out + weighted)
  ├── Ensemble-aware Scoring
  ├── Meta-Allocator family (FitnessWeighted, RegimeAware, etc.)
  ├── MutationOperator + Grok Creative Mutation
  ├── SimpleArena evolutionary loop
  └── Rich ASCII Visualization Dashboard

Layer 6: Monitoring & Observability (Active)
  ├── Live WebSocket Dashboard (`ftb-monitor`) — FastAPI + Tailwind + Chart.js — now matches rich CLI
  ├── Full real ArenaConfig passed from UI (allocator, creative_rate, adaptive, etc.)
  ├── PROGRESS_MAP.md rendered live inside the dashboard
  ├── Background real SimpleArena execution (threaded) streaming generation updates
  └── Start/Stop + persistence hooks ready for long experiments

Layer 7: Execution & Deployment (Future)
  ├── Broker integration (Alpaca / IBKR / Rockflow)
  ├── Paper trading loop
  └── Live execution + risk controls
```

---

## Current Build Status (Honest View)

| Layer | Component                                      | Status          | Notes |
|-------|--------------------------------------------------|-----------------|-------|
| 1     | Real Data Downloader                             | ✅ Done         | Yahoo Finance via yfinance |
| 1     | Synthetic Regime Generator                       | ✅ Done         | Supports heavy bias for stress testing |
| 2     | Backtesting Engine + MetaAllocator               | ✅ Done         | Full covariance + multiple allocator strategies |
| 3     | Agent Framework + Multiple Strategy Types        | ✅ Done         | Dalio + Momentum + MeanReversion + Defensive + creative variants |
| 4     | Validation Harness                               | ✅ Very Strong  | One of the strongest parts of the project |
| 5     | Population + Genomes                             | ✅ Done         | Core data structures solid |
| 5     | MultiAgentRunner + Ensemble Scoring (LOO)        | ✅ Done         | Real marginal contribution scoring working |
| 5     | Meta-Allocator Family                            | ✅ Done         | FitnessWeighted + RegimeAware implemented and integrated |
| 5     | Mutation + Grok Creative Mutation                | ✅ Functional   | Works, but creative mutations still too rare |
| 5     | SimpleArena Evolutionary Loop                    | ✅ Done         | Runs full generations on both synthetic and real data |
| 5     | Visualization / Dashboard                        | ✅ Excellent    | Rich terminal-style ASCII + matching Web dashboard (gen table ↑↓★, creative log, live charts, embedded PROGRESS_MAP) |
| 5     | Real-Data Arena Runs                             | ✅ Done         | 18-generation runs completed; fully configurable via CLI + Web |
| 5     | ArenaConfig + Persistence                        | ✅ Done         | Rich ArenaConfig (allocator, creative, adaptive, persistence_path); JSON save/load on Population |
| 6     | Broker / Paper Trading Integration               | ⬜ Not Started  | No execution layer yet |
| 6     | Long-running Experiments + Logging               | ⬜ Weak         | Currently manual |

---

## Phase 2 – Multi-Agent Arena (Current Sprint)

**Goal:** Build a population of heterogeneous trading agents that compete and evolve, where success is defined by **improving the overall portfolio** (risk-adjusted returns + drawdown control + diversification), not just individual agent performance.

### What's Working Well Right Now

- Full evolutionary loop on real historical data
- Proper ensemble-aware evaluation (not just individual Sharpe)
- Dynamic capital allocation via MetaAllocator
- Grok can propose genuinely new strategy variants (creative mutation)
- Rich terminal visualization/dashboard
- Validation harness is strong and already used on real data

### Current Limitations / Honest Gaps

- Creative mutations now trigger adaptively and survive better thanks to stronger bonus + controller (14/18 gens in recent runs had proposals).
- `ArenaConfig` + CLI + persistence now make long/reproducible experiments easy (`uv run python scripts/run_real_data_arena.py run --gens 20 --allocator regime_aware --save runs/`)
- `RegimeAwareAllocator` exists and is selectable; deeper coupling to live regime detection from engine data is the next natural step.
- Full AgentFactory + Registry is now live. Creative mutations intelligently propose and instantiate real distinct agents (DalioTactical, DalioWithTrendOverlay, RegimeRiskParity, etc.).
- System is now very close to "production research-grade" — persistence + rich config + dual CLI/Web paths complete the foundation.

### Recommended Next Focus Areas (in rough priority)

1. **Deepen Regime Awareness**
   - Couple RegimeAwareAllocator to real detected regimes from the backtest engine / synthetic labels
   - Stress-gen improvements (fat tails on transitions + explicit recovery phases)

2. **Full Multi-Type Agent Factory** ✅ Major progress
   - Registry + creative agents implemented and wired.
   - Next: Make creative proposals even smarter + richer behaviors for new types.

3. **Experiment Comparison & Resume**
   - Load saved populations and continue or compare runs side-by-side

4. **Paper Trading Path**
   - Alpaca (preferred) or Rockflow broker interface while keeping the same backtest code path

All the "do all those things" items requested (ArenaConfig richness, script wiring, persistence, rich web dashboard parity with CLI, background wiring) are now complete.

---

## Design Principles

- **Friendly First** — Capital preservation and robustness > raw returns
- **Ensemble Thinking** — An agent is valuable if it helps the *team*
- **Real Data Validation** — We only trust results that hold up on actual market history
- **Transparency** — Evolution decisions and creative proposals should be understandable

---

This map will be kept reasonably up to date as we continue building the arena.