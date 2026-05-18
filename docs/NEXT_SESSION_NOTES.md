# Next Session Handoff Notes – FriendlyTradeBot

**Date:** 2026-05-18 (end of session)
**User:** Rebooting machine + new session incoming

## Current Big Picture Status

- The "do all those things" phase (rich ArenaConfig, persistence, configurable CLI runs, monitoring dashboard) is **complete**.
- **Major recent win**: Full Agent Factory + Registry is now live and working.
  - All agents (foundational + creative) live under `src/friendly_trade_bot/agents/`
  - `REGISTRY` + `create_agent_from_genome()` is the single source of truth.
  - Creative mutations in `MutationOperator` now consult the registry and prefer proposing real evolved types.
  - `_instantiate_agent_from_genome()` in SimpleArena is now clean (just calls the registry).
  - New creative agents (`DalioTacticalAgent`, `DalioWithTrendOverlayAgent`, `RegimeRiskParityAgent`) have genuine behavioral differences.

- We just decided to move to **Regime Awareness** next (user chose option 3).

## What to Pick Up Next

The user explicitly chose to continue with **Regime Awareness**:

Priority items (from PROGRESS_MAP + conversation):
1. Couple `RegimeAwareAllocator` to actual detected regimes (from engine + synthetic labels).
2. Make `MultiAgentRunner` / `EnsembleScorer` actually pass regime context when calling `allocate()`.
3. Improve `RegimeAwareAllocator` preferences to intelligently use the new creative agents (e.g., favor `RegimeRiskParity` in crisis, `DalioTactical` in inflation/stagflation).
4. Add a simple regime detector helper (majority regime or last regime from the regimes DataFrame).
5. (Nice to have) Improve synthetic regime transitions (fat tails on switches + explicit recovery phases).

**Recommended first concrete coding step**:
- Add a `detect_regime(regimes_df)` helper.
- Update `MultiAgentRunner.run_population()` to compute a regime context and pass it to `meta_allocator.allocate(population, current_regime=...)`.
- Then enhance the preferences inside `RegimeAwareAllocator`.

## Important Code Locations

- Registry & Agents: `src/friendly_trade_bot/agents/registry.py`, `creative.py`, `simple.py`
- Creative logic: `src/friendly_trade_bot/arena/evolution.py` (`_generate_creative_variant`)
- Allocator: `src/friendly_trade_bot/arena/meta_allocator.py` (especially `RegimeAwareAllocator`)
- Runner: `src/friendly_trade_bot/arena/multi_agent_runner.py`
- Arena loop: `src/friendly_trade_bot/arena/simple_arena.py`
- Main script: `scripts/run_real_data_arena.py`

## Git State

- Many new files under `src/friendly_trade_bot/agents/` and arena modules were added in this session.
- User asked to commit + push everything before reboot.

## Other Notes

- The monitoring dashboard (`ftb-monitor`) is deprioritized for now — user prefers the rich CLI ASCII output.
- Persistence (Population.save/load) works but resume logic is still basic.
- Creative agents are functional but can be made richer over time.

## If You Get Lost

Read these first in the new session:
1. `docs/PROGRESS_MAP.md` (updated)
2. `docs/NEXT_SESSION_NOTES.md` (this file)
3. `src/friendly_trade_bot/agents/registry.py` (core of the recent big win)

Then ask the user: "We're in the middle of Regime Awareness work. Ready to continue with wiring the allocator to real regimes?"

Good luck in the new session. The project is in a strong state — the evolutionary loop is finally becoming real.