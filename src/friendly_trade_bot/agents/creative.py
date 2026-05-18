"""
Creative / evolved agent types proposed by the mutation system.

These are the first "real" children of the arena. They have genuine
behavioral differences that the EnsembleScorer and MetaAllocator
can actually reward or punish.
"""

from __future__ import annotations

from typing import Dict

import polars as pl

from friendly_trade_bot.agents.base import Agent, WorldState


class DalioTacticalAgent(Agent):
    """
    Dalio All-Weather with active tactical overlay.

    It watches recent equity momentum and the estimated portfolio vol
    (provided by the engine) to become more or less defensive than
    the static Dalio version.
    """

    def __init__(
        self,
        name: str = "DalioTactical",
        target_vol: float = 0.08,
        equity_reduction_in_stress: float = 0.40,
        trend_lookback: int = 20,
    ):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])
        self.target_vol = target_vol
        self.base_equity_reduction = equity_reduction_in_stress
        self.trend_lookback = trend_lookback

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        # Start from classic Dalio behavior
        base_reduction = self.base_equity_reduction

        # Tactical adjustment using trend
        spy_prices = world.prices.filter(pl.col("ticker") == "SPY").tail(self.trend_lookback)["close"].to_numpy()
        if len(spy_prices) >= self.trend_lookback:
            trend = (spy_prices[-1] / spy_prices[0]) - 1

            # If strong negative trend, become even more defensive
            if trend < -0.08:
                base_reduction = min(0.70, base_reduction + 0.20)
            # If strong positive trend, allow a bit more equity
            elif trend > 0.12:
                base_reduction = max(0.20, base_reduction - 0.10)

        # Use engine-provided vol signal if available
        if world.estimated_portfolio_vol and world.estimated_portfolio_vol > 0.18:
            base_reduction = min(0.75, base_reduction + 0.15)

        # Create a Dalio-like agent on the fly with modified stress parameter
        from friendly_trade_bot.agents.dalio_allweather import DalioAllWeatherAgent

        dalio = DalioAllWeatherAgent(
            name=self.name,
            target_vol=self.target_vol,
            equity_reduction_in_stress=base_reduction,
        )
        # We need to give it the same world view
        # Because DalioAllWeatherAgent doesn't take WorldState directly in a simple way,
        # we simulate the weights it would produce.
        # For simplicity we call its internal logic via a small trick:
        weights = dalio.observe(world)

        # Add a tiny tactical tilt toward gold in bad trends
        if "GLD" in weights and world.estimated_portfolio_vol and world.estimated_portfolio_vol > 0.15:
            weights["GLD"] = min(0.25, weights.get("GLD", 0.0) + 0.05)
            total = sum(weights.values())
            if total > 0:
                weights = {k: v / total * 0.95 for k, v in weights.items()}

        return weights


class DalioWithTrendOverlayAgent(Agent):
    """
    Classic Dalio All-Weather + a momentum overlay on the equity sleeve.

    Instead of treating all risk assets the same, it dynamically
    increases or decreases equity exposure based on recent trend strength.
    """

    def __init__(
        self,
        name: str = "DalioWithTrendOverlay",
        target_vol: float = 0.08,
        equity_reduction_in_stress: float = 0.40,
        momentum_lookback: int = 30,
        momentum_weight: float = 0.25,
    ):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])
        self.target_vol = target_vol
        self.equity_reduction_in_stress = equity_reduction_in_stress
        self.momentum_lookback = momentum_lookback
        self.momentum_weight = momentum_weight

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        from friendly_trade_bot.agents.dalio_allweather import DalioAllWeatherAgent

        # Get the base Dalio allocation
        dalio = DalioAllWeatherAgent(
            name=self.name,
            target_vol=self.target_vol,
            equity_reduction_in_stress=self.equity_reduction_in_stress,
        )
        base_weights = dalio.observe(world)

        # Compute momentum signal on SPY
        spy_prices = world.prices.filter(pl.col("ticker") == "SPY").tail(self.momentum_lookback)["close"].to_numpy()
        momentum_signal = 0.0
        if len(spy_prices) >= self.momentum_lookback:
            ret = (spy_prices[-1] / spy_prices[0]) - 1
            momentum_signal = max(-1.0, min(1.0, ret / 0.15))  # normalize roughly

        # Apply overlay: tilt equity exposure
        equity_tilt = momentum_signal * self.momentum_weight
        final_weights = base_weights.copy()

        if "SPY" in final_weights:
            final_weights["SPY"] = max(0.0, min(0.60, final_weights["SPY"] + equity_tilt * 0.4))

        # Re-normalize
        total = sum(final_weights.values())
        if total > 0:
            final_weights = {k: v / total * 0.95 for k, v in final_weights.items()}

        return final_weights


class RegimeRiskParityAgent(Agent):
    """
    Risk-parity style agent that explicitly changes its risk budget
    depending on the detected regime (provided by the engine via WorldState).
    """

    def __init__(
        self,
        name: str = "RegimeRiskParity",
        target_vol: float = 0.07,
        crisis_equity_cap: float = 0.15,
    ):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])
        self.target_vol = target_vol
        self.crisis_equity_cap = crisis_equity_cap

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        regime = (world.regime or "growth").lower()

        # Base risk-parity-ish allocation
        if regime in ("crisis", "stagflation"):
            weights = {
                "SPY": self.crisis_equity_cap,
                "TLT": 0.45,
                "IEI": 0.15,
                "GLD": 0.20,
                "DBC": 0.10,
            }
        elif regime == "inflation":
            weights = {
                "SPY": 0.20,
                "TLT": 0.20,
                "IEI": 0.15,
                "GLD": 0.25,
                "DBC": 0.20,
            }
        else:  # growth or deflation
            weights = {
                "SPY": 0.35,
                "TLT": 0.30,
                "IEI": 0.15,
                "GLD": 0.12,
                "DBC": 0.08,
            }

        # Light vol targeting
        if world.estimated_portfolio_vol and world.estimated_portfolio_vol > 0.12:
            scale = 0.12 / world.estimated_portfolio_vol
            weights = {k: v * scale for k, v in weights.items()}

        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total * 0.95 for k, v in weights.items()}

        return weights