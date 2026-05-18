"""
Evolutionary Operators for the Multi-Agent Arena.

This module handles how agents "evolve" over generations.

Now powered by the real AgentRegistry:
- Parameter mutation
- Type mutation between registered strategies
- Grok-assisted creative mutation that only proposes *real*, instantiable agent types
  (DalioTactical, RegimeRiskParity, DalioWithTrendOverlay, etc.)
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

from friendly_trade_bot.arena.population import AgentGenome
from friendly_trade_bot.agents.registry import REGISTRY


@dataclass
class MutationConfig:
    """Configuration for how aggressively to mutate genomes."""

    param_mutation_rate: float = 0.30
    param_mutation_strength: float = 0.15
    type_mutation_rate: float = 0.08
    creative_mutation_rate: float = 0.15      # Increased so creative mutations actually happen


class MutationOperator:
    """
    Applies mutations to AgentGenomes.

    This is the engine behind the evolutionary part of the arena.
    """

    def __init__(self, config: Optional[MutationConfig] = None):
        self.config = config or MutationConfig()

    def mutate(
        self,
        genome: AgentGenome,
        available_types: Optional[List[str]] = None,
        creative_rate: Optional[float] = None,
    ) -> tuple[AgentGenome, bool]:
        """
        Create a mutated copy of the genome.

        Args:
            creative_rate: Optional override for the creative mutation probability.
                           If provided, it overrides self.config.creative_mutation_rate.

        Returns:
            (new_genome, was_creative)
        """
        effective_creative_rate = creative_rate if creative_rate is not None else self.config.creative_mutation_rate

        new_params = genome.parameters.copy()
        mutated = False
        was_creative = False

        # 1. Parameter mutation
        for key, value in genome.parameters.items():
            if random.random() < self.config.param_mutation_rate:
                new_params[key] = self._mutate_value(value)
                mutated = True

        new_type = genome.agent_type

        # 2. Type mutation
        if available_types and random.random() < self.config.type_mutation_rate:
            other_types = [t for t in available_types if t != genome.agent_type]
            if other_types:
                new_type = random.choice(other_types)
                mutated = True

        # 3. Grok-assisted creative mutation (now accepts dynamic rate)
        if random.random() < effective_creative_rate:
            new_type, new_params = self._creative_mutation(genome, available_types)
            mutated = True
            was_creative = True

        if not mutated:
            new_params = self._force_small_mutation(new_params)

        new_genome = AgentGenome(
            agent_type=new_type,
            parameters=new_params,
            generation=genome.generation + 1,
            parent_ids=[genome.agent_type]
        )

        return new_genome, was_creative

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
        available_types: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> tuple[str, Dict[str, Any]]:
        """
        Grok-assisted creative mutation.

        This is where the real intelligence of the arena lives.

        Instead of just randomly tweaking numbers, we ask Grok (me) to propose
        thoughtful new strategy variants based on:
        - What the current best genome does
        - How it performed (especially in stress)
        - The broader market regime context

        The goal is to generate *novel but grounded* improvements rather than
        just Gaussian noise.
        """
        context = context or {}

        # Build a rich prompt describing the current champion
        prompt = self._build_creative_prompt(genome, context)

        # In a real deployment, this would be sent to Grok via API.
        # For now, we simulate thoughtful creative suggestions.
        new_type, new_params = self._generate_creative_variant(genome, available_types, context)

        print(f"\n[Grok Creative Mutation] Proposed new variant: {new_type}")
        print(f"  Reasoning: {prompt[:180]}...")  # Show part of the thinking

        return new_type, new_params

    def _build_creative_prompt(self, genome: AgentGenome, context: Dict[str, Any]) -> str:
        """Construct a high-quality prompt for Grok to generate creative mutations."""
        perf = context.get("recent_performance", {})
        stress_perf = context.get("stress_performance", {})

        # Tell the model what actually exists in the registry
        available = REGISTRY.get_available_types()
        creative_options = [t for t in available if t not in {"DalioAllWeather", "SimpleMomentum", "Defensive", "MeanReversion"}]

        prompt = (
            f"You are helping evolve a population of trading agents in the FriendlyTradeBot arena.\n\n"
            f"Current best genome:\n"
            f"- Type: {genome.agent_type}\n"
            f"- Parameters: {genome.parameters}\n"
            f"- Generation: {genome.generation}\n\n"
            f"Recent performance:\n"
            f"- CAGR: {perf.get('cagr', 'N/A')}\n"
            f"- Sharpe: {perf.get('sharpe', 'N/A')}\n"
            f"- Max Drawdown: {perf.get('max_dd', 'N/A')}\n\n"
            f"Stress test performance:\n"
            f"{stress_perf}\n\n"
            f"Currently registered strategy types in the system:\n"
            f"{available}\n\n"
            f"Especially interesting creative/evolved types available:\n"
            f"{creative_options or 'None yet — feel free to invent grounded new ones.'}\n\n"
            f"Task: Propose a novel but coherent evolution of this strategy. "
            f"Focus on improving robustness across regimes (especially crisis and stagflation). "
            f"Prefer proposing one of the creative types above when it makes sense, "
            f"or suggest a new well-named variant with sensible parameters.\n\n"
            f"Be creative but stay grounded in proper risk management and capital allocation principles."
        )
        return prompt

    def _generate_creative_variant(
        self,
        genome: AgentGenome,
        available_types: Optional[List[str]],
        context: Dict[str, Any],
    ) -> tuple[str, Dict[str, Any]]:
        """
        Intelligent creative variants powered by the AgentRegistry.

        Instead of hardcoding types, we now ask the registry what actually
        exists. This ensures creative mutations only propose real,
        instantiable strategies (including the new creative ones like
        DalioTactical, RegimeRiskParity, etc.).
        """
        params = genome.parameters.copy() or {}

        # Get the authoritative list from the registry
        all_registered = REGISTRY.get_available_types()

        # Separate foundational vs evolved/creative types
        foundational = {"DalioAllWeather", "SimpleMomentum", "Defensive", "MeanReversion"}
        creative_types = [t for t in all_registered if t not in foundational]

        new_type = genome.agent_type

        # Strong preference during creative mutation to propose a genuinely new evolved type
        if creative_types and random.random() < 0.75:
            # Prefer types the current population hasn't seen yet (promotes diversity)
            if available_types:
                unseen = [t for t in creative_types if t not in available_types]
                candidates = unseen or creative_types
            else:
                candidates = creative_types

            new_type = random.choice(candidates)

            # Seed parameters from the new type's registered defaults + keep useful parent params
            type_defaults = REGISTRY.get_defaults(new_type)
            if type_defaults:
                # Start fresh from the new type's defaults, then overlay any overlapping parent params
                params = {**type_defaults, **{k: v for k, v in params.items() if k in type_defaults}}

        # Apply some creative parameter evolution on top of whatever we have
        if "equity_reduction_in_stress" in params:
            params["equity_reduction_in_stress"] = round(
                max(0.30, min(0.70, params["equity_reduction_in_stress"] * random.uniform(0.85, 1.30))), 2
            )

        if "target_vol" in params:
            params["target_vol"] = round(
                max(0.05, min(0.14, params["target_vol"] * random.uniform(0.9, 1.15))), 3
            )

        # Occasionally add creative flags that some agents understand
        if random.random() < 0.4:
            params["creative_flag"] = True

        return new_type, params


# Convenience factory
def create_default_evolver() -> MutationOperator:
    return MutationOperator(MutationConfig())