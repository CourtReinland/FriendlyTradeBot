"""
Agent Registry – The central factory for creating agents from genomes.

This is the key piece that makes creative mutations actually produce
distinct, meaningful trading strategies instead of just renamed Dalio agents.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type

from friendly_trade_bot.agents.base import Agent
from friendly_trade_bot.agents.dalio_allweather import DalioAllWeatherAgent


# Type alias for a factory function that can build an agent from parameters
AgentFactory = Callable[[str, Dict[str, Any]], Agent]


class AgentRegistry:
    """
    Registry that maps agent_type strings to concrete agent implementations.

    This allows:
    - The arena to instantiate any genome (including creative proposals)
    - Easy extension with new strategy types
    - Clean separation between "genome DNA" and "live behavior"
    """

    def __init__(self):
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        agent_type: str,
        agent_class: Type[Agent],
        default_params: Optional[Dict[str, Any]] = None,
        factory: Optional[AgentFactory] = None,
    ) -> None:
        """
        Register a new agent type.

        Args:
            agent_type: Unique string identifier (e.g. "DalioTactical")
            agent_class: The Agent subclass
            default_params: Reasonable defaults when no params are provided
            factory: Optional custom factory function (genome_params -> Agent)
                     If not provided, we use a default that passes **params to the class.
        """
        if agent_type in self._registry:
            print(f"[AgentRegistry] Warning: overwriting existing type '{agent_type}'")

        def default_factory(name: str, params: Dict[str, Any]) -> Agent:
            # Merge defaults + provided params
            merged = {**(default_params or {}), **params}
            # Always pass name so the agent knows what creative type it is
            return agent_class(name=name, **merged)

        self._registry[agent_type] = {
            "class": agent_class,
            "defaults": default_params or {},
            "factory": factory or default_factory,
        }

    def create(self, agent_type: str, **params) -> Agent:
        """Create a live agent instance from a type + parameters."""
        if agent_type not in self._registry:
            # Graceful fallback: try to treat it as DalioAllWeather
            print(f"[AgentRegistry] Unknown type '{agent_type}', falling back to DalioAllWeather")
            agent_type = "DalioAllWeather"

        entry = self._registry[agent_type]
        factory = entry["factory"]
        return factory(agent_type, params)

    def get_defaults(self, agent_type: str) -> Dict[str, Any]:
        """Return the default parameters for a given type."""
        if agent_type not in self._registry:
            return {}
        return self._registry[agent_type]["defaults"].copy()

    def get_available_types(self) -> List[str]:
        """Return all registered agent type names."""
        return list(self._registry.keys())

    def is_registered(self, agent_type: str) -> bool:
        return agent_type in self._registry


# Global singleton registry used across the system
REGISTRY = AgentRegistry()


def register_default_agents():
    """
    Register all the agents we currently support.

    This is called once at import time so the rest of the system
    can rely on a populated registry.
    """
    # Core Dalio
    REGISTRY.register(
        "DalioAllWeather",
        DalioAllWeatherAgent,
        default_params={"target_vol": 0.08, "equity_reduction_in_stress": 0.40},
    )

    # Simple existing agents (imported below)
    try:
        from friendly_trade_bot.agents.simple import (
            SimpleMomentumAgent,
            DefensiveAgent,
            MeanReversionAgent,
        )

        REGISTRY.register(
            "SimpleMomentum",
            SimpleMomentumAgent,
            default_params={"lookback": 25, "target_vol": 0.09},
        )
        REGISTRY.register(
            "Defensive",
            DefensiveAgent,
            default_params={},
        )
        REGISTRY.register(
            "MeanReversion",
            MeanReversionAgent,
            default_params={"lookback": 12},
        )
    except ImportError:
        # Allow partial import during development
        pass

    # Creative / evolved types (will be implemented in creative.py)
    try:
        from friendly_trade_bot.agents.creative import (
            DalioTacticalAgent,
            DalioWithTrendOverlayAgent,
            RegimeRiskParityAgent,
        )

        REGISTRY.register(
            "DalioTactical",
            DalioTacticalAgent,
            default_params={
                "target_vol": 0.08,
                "equity_reduction_in_stress": 0.40,
                "trend_lookback": 20,
            },
        )
        REGISTRY.register(
            "DalioWithTrendOverlay",
            DalioWithTrendOverlayAgent,
            default_params={
                "target_vol": 0.08,
                "equity_reduction_in_stress": 0.40,
                "momentum_lookback": 30,
                "momentum_weight": 0.25,
            },
        )
        REGISTRY.register(
            "RegimeRiskParity",
            RegimeRiskParityAgent,
            default_params={
                "target_vol": 0.07,
                "crisis_equity_cap": 0.15,
            },
        )
    except ImportError:
        pass


# Auto-register on import
register_default_agents()


def create_agent_from_genome(genome) -> Agent:
    """
    Convenience function used by SimpleArena and population loading.
    """
    params = genome.parameters or {}
    return REGISTRY.create(genome.agent_type, **params)


# Expose the main entry points
__all__ = [
    "AgentRegistry",
    "REGISTRY",
    "register_default_agents",
    "create_agent_from_genome",
]