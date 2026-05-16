# FriendlyTradeBot

> A self-play arena of trading agents that compete, evolve, and allocate capital together — built for robustness, not prediction.

**Goal**: Proper, sustainable capital allocation in the age of AI. A "friendly" system that is hard to ruin, preserves capital across many regimes, and lets ordinary people participate in economic upside without needing to be quant wizards.

Inspired by:
- Ray Dalio's All-Weather risk-parity philosophy
- Jim Simons' data-driven, rigorous, edge-from-many-small-edges approach
- Noam Brown's Nash equilibrium self-play (Pluribus/Libratus) for imperfect-information multi-agent games
- AlphaGo Zero's recursive arena loop for monotonic improvement through self-play + strict evaluation

We treat markets as the imperfect-information, non-stationary, multi-agent game they actually are — closer to high-stakes poker than deterministic chess or Go.

---

## Current Status

**Phase 0 in progress** — laying professional foundations.

- [x] Git repo initialized + remote set to https://github.com/CourtReinland/FriendlyTradeBot
- [x] Reference materials imported (AlphaGo Zero summary + Noam Brown / Lex Fridman transcript)
- [ ] Python project structure + reproducible environment
- [ ] Data pipeline (core ETFs + synthetic regime generator)
- [ ] Production-grade backtester
- [ ] First "champion" agent (Dalio-inspired + regime awareness)
- [ ] Multi-agent arena + evolutionary improvement loop
- [ ] Rockflow paper trading integration

See the full [MVP Plan](https://github.com/CourtReinland/FriendlyTradeBot/blob/main/docs/PLAN.md) (or the local planning document) for detailed architecture, trade-offs, and phased roadmap.

---

## Why "Friendly"?

- **Capital preservation first** — drawdowns are the real enemy of long-term participation.
- **Regime robustness** — not optimized for the last 10 years, but designed to survive inflation, deflation, growth shocks, and AI-driven structural change.
- **Diversity as a feature** — a pool of intentionally different agents + dynamic meta-allocation (Dalio-style risk parity at the *strategy* level).
- **Monotonic improvement only** — new variants are only promoted if they demonstrably improve the *ensemble* on strict held-out stress scenarios (AlphaGo Zero discipline).
- **Explainable & auditable** — every promotion decision, every allocation change, every regime call is logged.

This is not a get-rich-quick black box. It is infrastructure for thoughtful, resilient capital allocation.

---

## Architecture (High Level)

```
Market Simulator (historical + synthetic regimes)
        ↓
Population of Agents (different "personalities")
        ↓
Meta-Allocator (dynamic risk budgeting across the pool)
        ↓
Arena Evaluator (only promote if ensemble improves on held-out data)
        ↓
Execution Layer (backtest → paper → live on Rockflow)
```

See `docs/ARCHITECTURE.md` (coming soon) for the full design.

---

## Getting Started (Once Phase 0 Completes)

```bash
# After cloning
uv sync          # or pip install -e .
python -m scripts.download_data
python -m scripts.run_single_agent_backtest
```

Full instructions will be in the README after the data + backtest layers land.

---

## Tech Philosophy

- **Python 3.12+**, Polars + Numba for speed where it matters.
- Custom fast simulator (not heavy frameworks) — multi-agent + custom synthetic data is easier this way.
- Every experiment is fully reproducible (config + git SHA + data version).
- Grok is used where it shines: clear reasoning, code that works, creative strategy mutation, and high-level oversight.
- No premature deep learning. We start with strong, interpretable, regime-aware systematic agents. Learned components earn their way in later.

---

## References

- [AlphaGo Zero summary](docs/AlphaGoSummary.md) — the recursive arena pattern we are adapting
- [Noam Brown on Poker, Nash, and Self-Play](docs/LexFridman-NoamBrown.md) (Lex Fridman Podcast #344) — why imperfect information + regret minimization matters for trading
- Ray Dalio "All Weather" portfolio construction (via Tony Robbins *Money: Master the Game*)
- Jim Simons / Renaissance Medallion principles distilled in various quant interviews
- Markov regime detection work (RohOnChain and others)

---

## Contributing

This is currently a focused collaboration. Once the MVP is live and paper-trading, we will open it up.

Until then: ideas, regime hypotheses, interesting stress scenarios, and brutal feedback on robustness are all welcome.

---

## License

To be decided after MVP. Likely MIT or a friendly open-source license that keeps the spirit of "capital allocation for normal people."

---

**Built late at night with Grok, for the long term.**

Good capital allocation is one of the most powerful forms of freedom in an AI-shaped world. Let's build something worthy of that.