# FriendlyTradeBot – Progress & Architecture Map

**Last Updated:** 2026-05-16  
**Current Focus:** Phase 2 – Multi-Agent Arena (Population + Ensemble-aware Scoring)

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
  ├── Real ETF Data Downloader          [DONE]
  │     └── SPY, TLT, IEI, GLD, DBC, ...
  └── Synthetic Regime Generator        [DONE]
        └── 5 regimes + adaptive stress biasing

Layer 2: Backtesting Engine (Core)
  ├── Event-driven simulation with realistic costs
  ├── Correlation-aware volatility targeting
  ├── Full rolling covariance matrix exposure
  └── Flexible rebalancing (daily/weekly/monthly)     [DONE]

Layer 3: Agents
  ├── Base Agent Protocol + WorldState
  └── DalioAllWeatherAgent (multi-signal stress detection)   [DONE]

Layer 4: Validation Harness (Very Strong)
  ├── Purged Walk-Forward (expanding + rich metrics)
  ├── Monte Carlo Permutation (Block Bootstrap + Adaptive block size)
  ├── Stress Testing + Recovery Analysis
  └── Unified ValidationReport + is_robust() heuristic     [DONE]

Layer 5: Multi-Agent Arena (Phase 2) ← CURRENT WORK
  ├── Population Manager
  ├── Ensemble-aware Scoring / Fitness
  ├── Evolutionary Operators (mutation, crossover, Grok-assisted)
  ├── Arena Evaluator (promotion gate)
  ├── Meta-Allocator (dynamic capital allocation)
  └── Self-Improvement Loop

Layer 6: Execution & Deployment (Future)
  ├── Rockflow Order Generation + Reconciliation
  ├── Risk Gates & Kill Switches
  └── Paper → Live Trading Loop
```

---

## Current Build Status

| Layer | Component                              | Status     | Notes |
|-------|----------------------------------------|------------|-------|
| 1     | Real Data Downloader                   | ✅ Done    | Works with real ETF history |
| 1     | Synthetic Regime Generator             | ✅ Done    | Supports stress biasing |
| 2     | Backtesting Engine                     | ✅ Done    | Correlation-aware + cov matrix |
| 3     | DalioAllWeatherAgent                   | ✅ Done    | Multi-signal stress detection |
| 4     | Validation Harness                     | ✅ Done    | WF + MC (Block Bootstrap) + Stress |
| 4     | Unified ValidationReport               | ✅ Done    | Nice summary + robustness heuristic |
| 5     | Arena – Population + Scoring           | 🚧 In Progress | Population + EnsembleScorer + basic MutationOperator |
| 5     | Arena – Evolution                      | ⬜ Not Started | - |
| 5     | Arena – Meta Allocator                 | ⬜ Not Started | - |
| 6     | Rockflow Execution                     | ⬜ Not Started | - |

---

## Phase 2 – Multi-Agent Arena (Current Sprint)

**Goal:** Build a population of trading agents that compete and evolve, where success is measured by **improving the overall portfolio**, not just individual performance.

### Current Work (Option 1)

We're starting with:

- **Population Manager** – Holds a collection of heterogeneous agents + their "genomes"
- **Ensemble-aware Scoring** – An agent is good if adding it improves the *total* portfolio's risk-adjusted return, drawdown, or diversification

### Next Pieces Planned

1. Population + Scoring (current)
2. Basic Evolutionary Operators (mutation + Grok-assisted mutation)
3. Arena Evaluator (promotion / demotion logic)
4. Meta-Allocator (dynamic capital allocation across the pool)
5. Full Self-Improvement Loop

---

## Design Principles

- **Friendly First**: Low ruin probability > high returns
- **Ensemble Thinking**: An agent is valuable if it *helps the team*
- **Robustness Over Optimization**: We care more about consistency across regimes than peak performance on one path
- **Transparency**: Every promotion/rejection should be explainable

---

## How to Read This Map

- ✅ = Fully working and tested
- 🚧 = Actively being built
- ⬜ = Planned but not started

This document will be kept up to date as we progress through the arena.

---

**Next Update Goal:** After Population + basic Ensemble Scoring is implemented.