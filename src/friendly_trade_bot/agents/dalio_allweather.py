"""
Dalio All-Weather inspired agent with volatility targeting and simple regime awareness.

This is the "champion" baseline agent for Phase 1.

Core philosophy (directly from Ray Dalio):
- Risk parity across economic regimes
- 30% Equities (growth)
- 55% Bonds (15% short/intermediate + 40% long duration)
- 7.5% Gold
- 7.5% Commodities

We add:
- Volatility targeting (target ~8% portfolio vol)
- Simple regime filter (reduce equity exposure in high-vol or inverted yield curve regimes)
- Conservative position limits suitable for a $10k account

This agent is intentionally "boring" and robust — exactly the kind of strategy that wins real competitions
and survives live trading (the Alpha Arena winning pattern).
"""

from __future__ import annotations

from datetime import date
from typing import Dict, Optional

import numpy as np
import polars as pl

from friendly_trade_bot.agents.base import Agent, WorldState


class DalioAllWeatherAgent(Agent):
    """
    Risk-parity style agent with volatility targeting and basic regime defense.

    Parameters
    ----------
    target_vol : float
        Target annualized portfolio volatility (default 8%)
    equity_reduction_in_stress : float
        How much to cut equity weight in bad regimes (0.0–1.0)
    """

    def __init__(
        self,
        name: str = "DalioAllWeather",
        target_vol: float = 0.08,
        equity_reduction_in_stress: float = 0.40,
    ):
        asset_universe = ["SPY", "TLT", "IEI", "GLD", "DBC"]
        super().__init__(name=name, asset_universe=asset_universe)

        self.target_vol = target_vol
        self.equity_reduction = equity_reduction_in_stress

        # Base Dalio risk-parity weights (before vol targeting)
        self.base_weights: Dict[str, float] = {
            "SPY": 0.30,
            "TLT": 0.40,   # Long bonds — big deflation hedge
            "IEI": 0.15,   # Intermediate bonds
            "GLD": 0.075,  # Gold
            "DBC": 0.075,  # Broad commodities
        }

    def reset(self) -> None:
        self._internal_state = {
            "last_rebalance": None,
            "vol_estimate": None,
        }

    def observe(self, world: WorldState) -> Dict[str, float]:
        """
        Decide target weights for today.

        Improvements in this version:
        - Data-driven stress detection (doesn't rely only on synthetic regime labels)
        - Uses equity-bond correlation breakdown as a signal
        - Uses the engine-provided covariance matrix when available
        - More graduated and conservative defense
        """
        weights = self.base_weights.copy()

        # === Improved Stress Detection ===
        stress_level = self._calculate_stress_level(world)

        if stress_level > 0.3:
            # Graduated defense based on stress intensity
            equity_cut = self.equity_reduction * min(stress_level, 1.0)
            weights["SPY"] *= (1.0 - equity_cut)

            # Boost defensives more aggressively in high stress
            defense_boost = 1.0 + (0.20 * stress_level)
            weights["TLT"] *= defense_boost
            weights["GLD"] *= (1.0 + 0.15 * stress_level)
            weights["DBC"] *= (1.0 + 0.12 * stress_level)

            # Slightly reduce intermediate bonds in extreme stress (curve flattening risk)
            if stress_level > 0.7:
                weights["IEI"] *= 0.90

        # === Correlation-aware Volatility Targeting ===
        current_portfolio_vol = (
            world.estimated_portfolio_vol or self._estimate_portfolio_vol(world)
        )

        if current_portfolio_vol and current_portfolio_vol > 0.01:
            vol_scalar = self.target_vol / current_portfolio_vol
            vol_scalar = max(0.35, min(1.20, vol_scalar))  # conservative bounds
            weights = {k: v * vol_scalar for k, v in weights.items()}

        # Normalize
        total = sum(weights.values())
        if total > 0.98:
            weights = {k: v * 0.98 / total for k, v in weights.items()}

        return weights

    def _calculate_stress_level(self, world: WorldState) -> float:
        """
        Returns a stress score between 0.0 and 1.0 based on multiple market signals.

        This is much more robust than just checking the synthetic regime label.
        """
        stress = 0.0
        signals = 0

        # 1. Use synthetic regime if available (strong signal during development)
        if world.regime in ["crisis", "stagflation"]:
            stress += 0.8
            signals += 1
        elif world.regime == "inflation":
            stress += 0.5
            signals += 1

        # 2. Recent SPY realized volatility (60-day)
        spv_prices = world.prices.filter(pl.col("ticker") == "SPY").tail(60)["close"].to_numpy()
        if len(spv_prices) > 25:
            rets = (spv_prices[1:] / spv_prices[:-1]) - 1
            vol = float(rets.std() * (252 ** 0.5))
            if vol > 0.25:
                stress += 0.7
            elif vol > 0.20:
                stress += 0.4
            signals += 1

        # 3. Equity-Bond correlation (rising correlation in stress is dangerous)
        if world.covariance_matrix is not None and world.covariance_tickers is not None:
            tickers = world.covariance_tickers
            try:
                sp_idx = tickers.index("SPY")
                tlt_idx = tickers.index("TLT")
                cov = world.covariance_matrix
                # Correlation = cov / (vol_spy * vol_tlt)
                vol_spy = np.sqrt(cov[sp_idx, sp_idx])
                vol_tlt = np.sqrt(cov[tlt_idx, tlt_idx])
                if vol_spy > 0 and vol_tlt > 0:
                    corr = cov[sp_idx, tlt_idx] / (vol_spy * vol_tlt)
                    if corr > 0.3:  # Normally equity-bond correlation is negative
                        stress += 0.6
                    signals += 1
            except (ValueError, IndexError):
                pass

        # 4. Simple yield curve proxy (TLT vs IEI relative strength)
        tlt_prices = world.prices.filter(pl.col("ticker") == "TLT").tail(40)["close"].to_numpy()
        iei_prices = world.prices.filter(pl.col("ticker") == "IEI").tail(40)["close"].to_numpy()
        if len(tlt_prices) > 20 and len(iei_prices) > 20:
            tlt_ret = (tlt_prices[-1] / tlt_prices[0]) - 1
            iei_ret = (iei_prices[-1] / iei_prices[0]) - 1
            # If long bonds are underperforming intermediate → curve flattening / inversion signal
            if tlt_ret < iei_ret - 0.02:
                stress += 0.35
            signals += 1

        # Normalize stress score
        if signals > 0:
            stress = min(stress / max(signals * 0.7, 1.0), 1.0)

        return float(stress)

    def _estimate_portfolio_vol(self, world: WorldState) -> Optional[float]:
        """
        Very rough 60-day portfolio volatility estimate.
        Good enough for Phase 1.
        """
        try:
            recent = world.prices.filter(pl.col("date") >= world.current_date).tail(60)
            vols = {}
            for ticker in self.asset_universe:
                t_prices = recent.filter(pl.col("ticker") == ticker)["close"].to_numpy()
                if len(t_prices) > 10:
                    rets = (t_prices[1:] / t_prices[:-1]) - 1
                    vols[ticker] = rets.std() * (252**0.5)

            if not vols:
                return None

            # Weighted average vol (very crude, ignores correlations)
            port_vol = sum(self.base_weights.get(t, 0) * vols.get(t, 0.15) for t in self.asset_universe)
            return float(port_vol)
        except Exception:
            return 0.15  # fallback


# Factory for convenience
def create_dalio_agent(target_vol: float = 0.08) -> DalioAllWeatherAgent:
    return DalioAllWeatherAgent(target_vol=target_vol)