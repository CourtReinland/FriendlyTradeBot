"""
FriendlyTradeBot Agents Package

This package contains all trading agents and the central registry
that turns AgentGenomes into live strategy instances.

The registry is what makes creative evolution actually produce
different behaviors instead of just different names.
"""

from __future__ import annotations

# Core interface
from .base import Agent, WorldState, AgentProtocol

# Registry (the heart of the agent factory)
from .registry import (
    AgentRegistry,
    REGISTRY,
    register_default_agents,
    create_agent_from_genome,
)

# Core agents
from .dalio_allweather import DalioAllWeatherAgent

# Simple diverse agents
from .simple import SimpleMomentumAgent, DefensiveAgent, MeanReversionAgent

# Creative / evolved agents (the payoff of the evolutionary system)
from .creative import (
    DalioTacticalAgent,
    DalioWithTrendOverlayAgent,
    RegimeRiskParityAgent,
)

__all__ = [
    # Base
    "Agent",
    "WorldState",
    "AgentProtocol",
    # Registry
    "AgentRegistry",
    "REGISTRY",
    "register_default_agents",
    "create_agent_from_genome",
    # Concrete agents
    "DalioAllWeatherAgent",
    "SimpleMomentumAgent",
    "DefensiveAgent",
    "MeanReversionAgent",
    "DalioTacticalAgent",
    "DalioWithTrendOverlayAgent",
    "RegimeRiskParityAgent",
]