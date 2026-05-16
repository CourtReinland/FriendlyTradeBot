"""
Evolutionary Operators for the Multi-Agent Arena.

This module handles how agents "evolve" over generations.

Current capabilities:
- Parameter mutation (Gaussian noise on numeric hyperparameters)
- Strategy type mutation (occasional change of agent species)
- Placeholder for Grok-assisted creative mutation (the most powerful future direction)
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from friendly_trade_bot.arena.population import AgentGenome


@dataclass
class MutationConfig:
    """Configuration for how aggressively to mutate genomes."""

    param_mutation_rate: float = 0.3          # Probability a parameter gets mutated
    param_mutation_strength: float = 0.15     # Std dev of Gaussian noise (relative)
    type_mutation_rate: float = 0.08          # Chance to change agent_type entirely
    creative_mutation_rate: float = 0.05      # Chance to trigger "Grok-assisted" creative jump


class MutationOperator:
    """
    Applies mutations to AgentGenomes.

    This is the engine behind the evolutionary part of the arena.
    """

    def __init__(self, config: Optional[MutationConfig] = None):
        self.config = config or MutationConfig()

    def mutate(self, genome: AgentGenome, available_types: Optional[List[str]] = None) -> AgentGenome:
        """
        Create a mutated copy of the genome.

        Args:
            genome: The parent genome
            available_types: List of possible agent_type strings (for type mutation)
        """
        new_params = genome.parameters.copy()
        mutated = False

        # 1. Parameter mutation (most common)
        for key, value in genome.parameters.items():
            if random.random() < self.config.param_mutation_rate:
                new_params[key] = self._mutate_value(value)
                mutated = True

        new_type = genome.agent_type

        # 2. Occasional strategy type mutation
        if available_types and random.random() < self.config.type_mutation_rate:
            other_types = [t for t in available_types if t != genome.agent_type]
            if other_types:
                new_type = random.choice(other_types)
                mutated = True

        # 3. Creative (Grok-assisted) mutation placeholder
        if random.random() < self.config.creative_mutation_rate:
            new_type, new_params = self._creative_mutation(genome, available_types)
            mutated = True

        if not mutated:
            # Force a small mutation if nothing happened
            new_params = self._force_small_mutation(new_params)

        return AgentGenome(
            agent_type=new_type,
            parameters=new_params,
            generation=genome.generation + 1,
            parent_ids=[genome.agent_type]  # simplified lineage
        )

    def _mutate_value(self, value: Any) -> Any:
        """Apply Gaussian noise to numeric values, leave others mostly untouched."""
        if isinstance(value, (int, float)):
            noise = np.random.normal(0, abs(value) * self.config.param_mutation_strength + 0.01)
            new_value = value + noise
            # Keep integers as integers when appropriate
            if isinstance(value, int) and abs(new_value - round(new_value)) < 0.1:
                return int(round(new_value))
            return float(new_value)
        elif isinstance(value, bool):
            return not value if random.random() < 0.1 else value
        else:
            return value

    def _force_small_mutation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Guarantee at least one small change."""
        if not params:
            return params
        key = random.choice(list(params.keys()))
        params[key] = self._mutate_value(params[key])
        return params

    def _creative_mutation(
        self,
        genome: AgentGenome,
        available_types: Optional[List[str]] = None
    ) -> tuple[str, Dict[str, Any]]:
        """
        Placeholder for Grok-assisted creative mutation.

        In the future, this will call Grok with something like:
            "Given this winning genome: {genome}, propose a novel but related
             trading strategy variant that might perform well in stagflation."

        For now, it does a more aggressive parameter change + possible type switch.
        """
        new_params = {}
        for k, v in genome.parameters.items():
            # More aggressive mutation
            if isinstance(v, (int, float)):
                new_params[k] = v * random.uniform(0.6, 1.7)
            else:
                new_params[k] = v

        new_type = genome.agent_type
        if available_types and len(available_types) > 1:
            new_type = random.choice([t for t in available_types if t != genome.agent_type])

        return new_type, new_params


# Convenience factory
def create_default_evolver() -> MutationOperator:
    return MutationOperator(MutationConfig())