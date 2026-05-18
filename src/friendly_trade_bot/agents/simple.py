"""
Simple but useful trading agents used for diversity in the arena.

These are intentionally lightweight. They demonstrate different "personalities"
that the meta-allocator can combine.
"""

from __future__ import annotations

from typing import Dict

import polars as pl

from friendly_trade_bot.agents.base import Agent, WorldState


class SimpleMomentumAgent(Agent):
    """Goes long equities when recent trend is positive."""

    def __init__(self, name: str = "Momentum", lookback: int = 20, target_vol: float = 0.10):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])
        self.lookback = lookback
        self.target_vol = target_vol

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        weights = {t: 0.0 for t in self.asset_universe}

        spy_prices = world.prices.filter(pl.col("ticker") == "SPY").tail(self.lookback)["close"].to_numpy()
        if len(spy_prices) < self.lookback:
            weights["SPY"] = 0.3
            return weights

        trend = (spy_prices[-1] / spy_prices[0]) - 1

        if trend > 0.02:
            weights["SPY"] = 0.6
            weights["TLT"] = 0.15
            weights["GLD"] = 0.1
        else:
            weights["TLT"] = 0.5
            weights["IEI"] = 0.3
            weights["GLD"] = 0.15

        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total * 0.95 for k, v in weights.items()}

        return weights


class DefensiveAgent(Agent):
    """Stays defensive – heavy in bonds and gold."""

    def __init__(self, name: str = "Defensive"):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        return {
            "SPY": 0.10,
            "TLT": 0.45,
            "IEI": 0.20,
            "GLD": 0.15,
            "DBC": 0.05,
        }


class MeanReversionAgent(Agent):
    """Bets against recent extreme moves in equities."""

    def __init__(self, name: str = "MeanReversion", lookback: int = 10):
        super().__init__(name=name, asset_universe=["SPY", "TLT", "IEI", "GLD", "DBC"])
        self.lookback = lookback

    def reset(self):
        self._internal_state = {}

    def observe(self, world: WorldState) -> Dict[str, float]:
        weights = {t: 0.0 for t in self.asset_universe}

        spy_prices = world.prices.filter(pl.col("ticker") == "SPY").tail(self.lookback)["close"].to_numpy()
        if len(spy_prices) < 5:
            weights["TLT"] = 0.5
            weights["IEI"] = 0.4
            return weights

        recent_return = (spy_prices[-1] / spy_prices[0]) - 1

        if recent_return > 0.04:
            weights["SPY"] = -0.2   # conceptually short via bonds
            weights["TLT"] = 0.6
            weights["GLD"] = 0.25
        elif recent_return < -0.04:
            weights["SPY"] = 0.5
            weights["TLT"] = 0.3
            weights["DBC"] = 0.1
        else:
            weights["TLT"] = 0.5
            weights["IEI"] = 0.4

        total = sum(abs(v) for v in weights.values())
        if total > 0:
            weights = {k: v / total * 0.9 for k, v in weights.items()}

        return weights