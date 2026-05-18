"""
Base Agent interface for FriendlyTradeBot.

Every trading agent (Dalio All-Weather, momentum, defensive, etc.) must implement
this protocol. This allows the backtest engine, arena, and meta-allocator to treat
all agents uniformly.

Design goals:
- Simple, explicit interface
- Agents are stateful (they can maintain internal state across days)
- Agents receive a "World" view (prices, current portfolio, regime info)
- Agents return target portfolio weights (not raw orders) — the engine handles sizing
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Protocol

import numpy as np
import polars as pl


@dataclass
class WorldState:
    """
    Snapshot of the world an agent sees on a given decision date.

    This is the primary input to every agent.
    """

    current_date: date
    prices: pl.DataFrame
    portfolio_value: float
    current_weights: Dict[str, float]
    cash: float

    # Regime information
    regime: Optional[str] = None
    regime_id: Optional[int] = None

    # Engine-provided diagnostics (very useful for vol targeting)
    estimated_portfolio_vol: Optional[float] = None   # annualized, correlation-aware
    asset_vols: Optional[Dict[str, float]] = None     # individual asset vols
    recent_correlation: Optional[float] = None        # average pairwise correlation (optional)

    # Advanced: Full covariance matrix for sophisticated agents
    # Shape: (n_assets, n_assets), annualized
    covariance_matrix: Optional[np.ndarray] = None
    covariance_tickers: Optional[List[str]] = None


class Agent(ABC):
    """
    Abstract base class for all trading agents.

    Agents are expected to be:
    - Stateless with respect to the engine (they manage their own internal state)
    - Deterministic given the same WorldState + seed
    - Focused on producing target weights, not execution
    """

    name: str
    asset_universe: list[str]

    def __init__(self, name: str, asset_universe: list[str]):
        self.name = name
        self.asset_universe = asset_universe
        self._internal_state: dict = {}  # Agents can store whatever they need here

    @abstractmethod
    def reset(self) -> None:
        """Reset any internal state (called at the start of a new backtest episode)."""
        self._internal_state = {}

    @abstractmethod
    def observe(self, world: WorldState) -> Dict[str, float]:
        """
        Given the current world state, return target portfolio weights.

        Returns:
            Dict[ticker, target_weight] where weights should sum to <= 1.0
            (any remainder stays in cash).

        The engine will later translate these weights into actual positions
        while respecting risk limits, slippage, and capital constraints.
        """
        ...

    def get_state(self) -> dict:
        """Return a copy of internal state for logging / debugging."""
        return self._internal_state.copy()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"


class AgentProtocol(Protocol):
    """
    Structural typing version of Agent for more flexible use (e.g. with functions).
    """

    name: str
    asset_universe: list[str]

    def reset(self) -> None: ...
    def observe(self, world: WorldState) -> Dict[str, float]: ...


# Type alias for convenience
TradingAgent = Agent | AgentProtocol