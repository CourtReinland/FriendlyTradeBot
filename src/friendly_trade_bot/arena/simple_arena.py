"""
SimpleArena – The first working version of the multi-agent evolutionary loop.

This is the core "self-improving population of trading bots" mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from friendly_trade_bot.arena.creative_rate_controller import CreativeRateController, CreativeRateConfig
from friendly_trade_bot.arena.evolution import MutationOperator
from friendly_trade_bot.arena.meta_allocator import MetaAllocator
from friendly_trade_bot.arena.population import Population
from friendly_trade_bot.arena.scoring import EnsembleScorer
from friendly_trade_bot.arena.visualization import track_generation, print_evolution_dashboard
from friendly_trade_bot.backtest.engine import BacktestEngine


@dataclass
class ArenaConfig:
    """Highly configurable settings for the evolutionary arena.

    Supports full control over population dynamics, creative exploration,
    meta-allocation strategy, and basic persistence for long runs.
    """

    # Core population dynamics
    population_size: int = 12
    keep_top_n: int = 6
    generations: int = 12

    mutation_rate: float = 0.60

    # Creative mutation (Grok-assisted novel strategy proposals)
    creative_mutation_rate: float = 0.15          # Base rate (dynamically adjusted if adaptive)
    creative_fitness_boost: float = 0.075         # Stronger temporary boost for new creative agents
    exploration_bonus: float = 0.075              # Passed to controller; higher = more aggressive creative survival

    track_history: bool = True

    # Adaptive creative rate controller (stagnation → higher exploration)
    use_adaptive_creative_rate: bool = True
    creative_rate_config: CreativeRateConfig = None  # Full control over stagnation detection

    # Meta allocation strategy across the population
    meta_allocator_type: str = "fitness_weighted"  # "equal", "fitness_weighted", "regime_aware"

    # Persistence (basic experiment saving)
    persistence_path: Optional[str] = None        # If set, save population JSON after each generation
    save_every_n_generations: int = 1

    # Misc
    seed: Optional[int] = None


class SimpleArena:
    """
    A basic evolutionary arena for trading agents.

    Supports MetaAllocator and now includes optional evolution visualization.
    """

    def __init__(
        self,
        engine: BacktestEngine,
        scorer: EnsembleScorer,
        mutator: MutationOperator,
        config: Optional[ArenaConfig] = None,
        meta_allocator: Optional[MetaAllocator] = None,
        generation_callback: Optional[callable] = None,   # Called after each generation with update dict
    ):
        self.engine = engine
        self.scorer = scorer
        self.mutator = mutator
        self.config = config or ArenaConfig()
        self.generation_callback = generation_callback

        self.history: List[dict] = []
        self.creative_generations: set = set()

        # Resolve meta_allocator from explicit instance or from config string
        if meta_allocator is not None:
            self.meta_allocator = meta_allocator
        else:
            self.meta_allocator = self._create_meta_allocator_from_config()

        if self.meta_allocator and hasattr(self.scorer, "runner"):
            self.scorer.runner.meta_allocator = self.meta_allocator

        creative_cfg = self.config.creative_rate_config or CreativeRateConfig(
            base_rate=self.config.creative_mutation_rate,
            max_rate=0.40,
            exploration_bonus=self.config.exploration_bonus or self.config.creative_fitness_boost,
        )
        self.creative_controller = CreativeRateController(creative_cfg) if self.config.use_adaptive_creative_rate else None

    def run_generation(self, population: Population, price_data, regimes=None) -> Population:
        """
        Run one full generation of evolution.
        """
        print(f"\n[SimpleArena] Running generation {population.generation} "
              f"(size={len(population)})")

        # 1. Evaluate the population (ensemble scoring)
        scores = self.scorer.evaluate_population(population, price_data, regimes)

        # 2. Sort agents by fitness (best first)
        sorted_members = population.get_sorted_by_fitness(descending=True)

        # 3. Select survivors (top N)
        survivors = sorted_members[: self.config.keep_top_n]

        print(f"  Top {len(survivors)} agents kept. Best fitness: "
              f"{survivors[0].fitness:.4f}" if survivors and survivors[0].fitness else "N/A")

        # 4. Create new population
        new_population = Population(name=population.name)
        new_population.generation = population.generation + 1

        # Keep the survivors (preserve their fitness from the just-completed evaluation)
        for member in survivors:
            new_population.add_agent(
                agent=member.agent,
                genome=member.genome,
                agent_id=member.id,
                fitness=member.fitness,
                individual_metrics=member.individual_metrics,
            )

        # 5. Fill the rest of the population with mutated offspring
        num_offspring = self.config.population_size - len(survivors)

        available_types = list(set(m.genome.agent_type for m in sorted_members))

        # Determine current creative mutation rate (adaptive if enabled)
        current_creative_rate = self.config.creative_mutation_rate
        if self.creative_controller:
            current_creative_rate = self.creative_controller.get_current_rate()

        creative_happened_this_gen = False

        for i in range(num_offspring):
            parent = survivors[i % len(survivors)]

            # Mutate with the current (possibly boosted) creative rate
            new_genome, was_creative = self.mutator.mutate(
                parent.genome,
                available_types=available_types,
                creative_rate=current_creative_rate if self.creative_controller else None
            )

            if was_creative:
                creative_happened_this_gen = True

            new_agent = self._instantiate_agent_from_genome(new_genome)
            new_id = f"{new_genome.agent_type}_gen{new_population.generation}_{i}"

            # Apply stronger exploration bonus for creative mutants
            initial_fitness = self.config.creative_fitness_boost if was_creative else None

            new_population.add_agent(
                agent=new_agent,
                genome=new_genome,
                agent_id=new_id,
                fitness=initial_fitness
            )

        print(f"  Created {num_offspring} new mutated agents.")

        # Track history + feed adaptive creative controller
        if self.config.track_history:
            current_rate = current_creative_rate if self.creative_controller else self.config.creative_mutation_rate

            if creative_happened_this_gen:
                self.creative_generations.add(new_population.generation)

            entry = {
                "generation": new_population.generation,
                "type_counts": {m.genome.agent_type: sum(1 for x in new_population.members.values() if x.genome.agent_type == m.genome.agent_type) for m in new_population.members.values()},
                "best_fitness": max((m.fitness or 0.0) for m in new_population.members.values()),
                "avg_fitness": sum(m.fitness or 0.0 for m in new_population.members.values()) / max(len(new_population), 1),
                "size": len(new_population),
                "creative_mutation": creative_happened_this_gen,
                "creative_rate": current_rate,
            }

            self.history.append(entry)

            if self.creative_controller:
                self.creative_controller.update(entry)

            # Send live update if a callback is registered (used by the monitoring dashboard)
            if self.generation_callback:
                update = {
                    "generation": entry["generation"],
                    "best_fitness": entry["best_fitness"],
                    "avg_fitness": entry["avg_fitness"],
                    "creative_rate": entry.get("creative_rate"),
                    "size": entry["size"],
                    "creative_mutation": entry["creative_mutation"],
                    "type_counts": entry["type_counts"],
                }
                try:
                    self.generation_callback(update)
                except Exception as e:
                    print(f"[SimpleArena] generation_callback error: {e}")

        return new_population

    def _create_meta_allocator_from_config(self):
        """Factory for MetaAllocator based on ArenaConfig.meta_allocator_type."""
        from friendly_trade_bot.arena.meta_allocator import (
            EqualWeightAllocator,
            FitnessWeightedAllocator,
            RegimeAwareAllocator,
            create_default_meta_allocator,
        )

        t = (self.config.meta_allocator_type or "fitness_weighted").lower()
        if t in ("equal", "equal_weight"):
            return EqualWeightAllocator()
        elif t in ("regime", "regime_aware"):
            return RegimeAwareAllocator()
        else:
            # Default and "fitness_weighted"
            return create_default_meta_allocator()

    def _instantiate_agent_from_genome(self, genome):
        """
        Create a live agent from a genome using the central AgentRegistry.

        This is now the real factory. Creative mutations that propose
        "DalioTactical", "RegimeRiskParity", etc. will actually get
        different behavioral implementations.
        """
        from friendly_trade_bot.agents.registry import create_agent_from_genome

        return create_agent_from_genome(genome)

    def run(self, initial_population: Population, price_data, regimes=None) -> Population:
        """
        Run the arena for multiple generations.
        """
        current_pop = initial_population

        for gen in range(self.config.generations):
            current_pop = self.run_generation(current_pop, price_data, regimes)

        print(f"\n[SimpleArena] Finished {self.config.generations} generations.")

        # Show rich dashboard visualization
        if self.config.track_history and self.history:
            from friendly_trade_bot.arena.visualization import print_evolution_dashboard
            print_evolution_dashboard(self.history, title="ARENA EVOLUTION DASHBOARD")

        return current_pop