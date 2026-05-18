"""
Demo Agents – Re-exports from the canonical package.

All real agent implementations now live in src/friendly_trade_bot/agents/.
This file is kept for backward compatibility with older scripts.
"""

from friendly_trade_bot.agents import (
    SimpleMomentumAgent,
    DefensiveAgent,
    MeanReversionAgent,
    DalioAllWeatherAgent,
    DalioTacticalAgent,
    DalioWithTrendOverlayAgent,
    RegimeRiskParityAgent,
)

__all__ = [
    "SimpleMomentumAgent",
    "DefensiveAgent",
    "MeanReversionAgent",
    "DalioAllWeatherAgent",
    "DalioTacticalAgent",
    "DalioWithTrendOverlayAgent",
    "RegimeRiskParityAgent",
]
