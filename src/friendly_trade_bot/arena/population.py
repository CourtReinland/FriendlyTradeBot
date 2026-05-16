"""
Population – Manages a collection of trading agents in the arena.

This is the central data structure for Phase 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from friendly_trade_bot.agents.base import Agent


@dataclass
class AgentGenome:
    """
    Represents the "DNA" of an agent.

    For now this is simple (strategy type + parameters).
    Later this can be expanded to support code generation, neural net weights, etc.
    """
    agent_type: str                    # e.g. "DalioAllWeather", "Momentum", "VolatilityBreakout"
    parameters: Dict[str, Any]         # hyperparameters / weights / thresholds
    generation: int = 0
    parent_ids: List[str] = field(default_factory=list)


@dataclass
class AgentMember:
    """A member of the population."""
    agent: Agent
    genome: AgentGenome
    id: str
    fitness: Optional[float] = None           # ensemble contribution score
    individual_metrics: Optional[Dict[str, float]] = None


class Population:
    """
    A population of trading agents.

    Responsibilities:
    - Hold agents + their genomes
    - Track fitness scores (ensemble contribution)
    - Provide methods for selection, addition, removal
    """

    def __init__(self, name: str = "MainPopulation"):
        self.name = name
        self.members: Dict[str, AgentMember] = {}
        self.generation: int = 0

    def add_agent(self, agent: Agent, genome: AgentGenome, agent_id: Optional[str] = None) -> str:
        """Add a new agent to the population."""
        if agent_id is None:
            agent_id = f"{genome.agent_type}_{len(self.members)}"

        member = AgentMember(
            agent=agent,
            genome=genome,
            id=agent_id,
        )
        self.members[agent_id] = member
        return agent_id

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the population."""
        return self.members.pop(agent_id, None) is not None

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        member = self.members.get(agent_id)
        return member.agent if member else None

    def get_fitness(self, agent_id: str) -> Optional[float]:
        member = self.members.get(agent_id)
        return member.fitness if member else None

    def set_fitness(self, agent_id: str, fitness: float, metrics: Optional[Dict[str, float]] = None):
        """Update the ensemble fitness of an agent."""
        if agent_id in self.members:
            self.members[agent_id].fitness = fitness
            if metrics:
                self.members[agent_id].individual_metrics = metrics

    def get_all_agents(self) -> List[Agent]:
        return [m.agent for m in self.members.values()]

    def get_sorted_by_fitness(self, descending: bool = True) -> List[AgentMember]:
        """Return members sorted by fitness (best first by default)."""
        sorted_members = sorted(
            self.members.values(),
            key=lambda m: m.fitness if m.fitness is not None else -float("inf"),
            reverse=descending
        )
        return sorted_members

    def __len__(self):
        return len(self.members)

    def __repr__(self):
        return f"Population(name={self.name}, size={len(self)}, generation={self.generation})"