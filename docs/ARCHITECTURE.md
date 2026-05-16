# FriendlyTradeBot Architecture (Living Document)

**Status**: Early Phase 0 — foundations being laid. This document will evolve with the implementation.

See the full [MVP Plan](../README.md#current-status) (or the detailed planning document in the session) for the complete rationale, trade-off analysis, and phased roadmap.

## Core Philosophy

1. **Markets are imperfect-information, multi-agent, non-stationary games** (closer to Pluribus poker than AlphaGo Go).
2. **Robustness > prediction**. A strategy that survives many possible futures with acceptable drawdowns is more valuable than one that maximizes returns on the single historical path we happened to observe.
3. **Diversity is the feature**. A pool of agents with different "personalities" + a meta-allocator that treats them like asset classes (Dalio risk-parity at strategy level) is the practical way to implement antifragility.
4. **Monotonic improvement only** (AlphaGo Zero arena discipline). New variants are only promoted if they improve the *ensemble* on strict held-out stress scenarios (including synthetic regimes).
5. **"Friendly" means low ruin probability**. The system must be something a normal person can actually run for years without blowing up or losing sleep.

## High-Level Components

- **Data Layer** (`src/data/`)
  - Historical ETF / macro data (Yahoo, FRED, etc.)
  - Synthetic regime-switching generator (critical for honest robustness testing)

- **Backtest Engine** (`src/backtest/`)
  - Fast vectorized + event-driven hybrid simulator
  - Realistic costs (slippage, commissions, gaps)
  - "World" abstraction that multiple agents can observe and act upon

- **Agents** (`src/agents/`)
  - Base protocol: `observe(state) -> action` (target weights or orders)
  - Seeded species: Dalio All-Weather + regime filter, momentum, duration timer, defensive, etc.
  - Later: learned value functions, policy heads

- **Arena + Evolution** (`src/arena/`)
  - Multi-agent episode runner
  - Strict evaluator (promotion gate — 55% style threshold on ensemble metrics)
  - Evolutionary operators + Grok-assisted creative mutation

- **Meta Allocator** (`src/meta/`)
  - Dynamic capital allocation across the current champion pool (inverse vol, risk budgeting, regime-conditioned)

- **Execution** (`src/execution/`)
  - Abstract `Broker` interface
  - Rockflow concrete implementation
  - Same code path for backtest / paper / live

- **Utils**
  - Config (Pydantic), experiment provenance (git SHA + config JSON), logging, metrics

## Key Design Decisions (Early)

- **Python 3.12+ + Polars + Numba**: Fast enough for thousands of Monte Carlo episodes per generation on a laptop.
- **Custom simulator** (not Backtrader/Zipline): Needed for clean multi-agent interaction + easy synthetic regime injection.
- **Pydantic configs everywhere**: Every experiment is fully reproducible.
- **No premature neural nets**: Strong systematic agents first. Learned components must prove they improve held-out ensemble metrics.
- **Grok as creative partner**: Used for strategy hypothesis generation, mutation suggestions, narrative explanations, and high-level oversight — not as the inner-loop order placer in MVP.

## Next Documents (Planned)

- `BACKTEST_ENGINE.md` — detailed spec of the simulator
- `AGENT_SPEC.md` — interface + first 4–6 seeded species
- `ARENA_EVALUATOR.md` — exact promotion criteria and statistical tests
- `ROCKFLOW_INTEGRATION.md`

This architecture is deliberately pragmatic. We are building something that can be paper-traded responsibly within weeks, not a research moonshot that never ships.