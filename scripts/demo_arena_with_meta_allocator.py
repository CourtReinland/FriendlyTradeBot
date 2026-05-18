"""
Demo: SimpleArena with MetaAllocator Integration

This script shows the current state of the Multi-Agent Arena (Phase 2):

- A population of agents (variations of DalioAllWeather)
- Ensemble-aware scoring via Leave-One-Out (MultiAgentRunner)
- Dynamic capital allocation via MetaAllocator (FitnessWeighted)
- Evolutionary loop (SimpleArena) with mutation

Run this to see the arena actually evolve a population over generations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import polars as pl

from friendly_trade_bot.agents.dalio_allweather import DalioAllWeatherAgent
from friendly_trade_bot.arena import (
    ArenaConfig,
    EnsembleScorer,
    MultiAgentRunner,
    MutationOperator,
    Population,
    SimpleArena,
    create_default_meta_allocator,
)
from friendly_trade_bot.arena.population import AgentGenome
from friendly_trade_bot.arena.population import AgentGenome
from friendly_trade_bot.backtest.engine import BacktestConfig, BacktestEngine
from friendly_trade_bot.data.synthetic import generate_regime_dataframe


def create_diverse_population(size: int = 8) -> Population:
    """Create a starting population with some variation in parameters."""
    pop = Population(name="DalioPopulation_v1")

    base_params = {
        "target_vol": 0.08,
        "equity_reduction_in_stress": 0.40,
    }

    for i in range(size):
        # Create some natural variation
        params = base_params.copy()
        params["target_vol"] = round(np.random.uniform(0.06, 0.11), 3)
        params["equity_reduction_in_stress"] = round(np.random.uniform(0.30, 0.55), 2)

        genome = AgentGenome(
            agent_type="DalioAllWeather",
            parameters=params,
            generation=0,
        )

        agent = DalioAllWeatherAgent(
            name=f"Dalio_{i}",
            target_vol=params["target_vol"],
            equity_reduction_in_stress=params["equity_reduction_in_stress"],
        )

        pop.add_agent(agent, genome, agent_id=f"dalio_{i}")

    return pop


def main():
    print("=" * 65)
    print("FriendlyTradeBot Arena Demo — With MetaAllocator")
    print("=" * 65 + "\n")

    # 1. Generate synthetic data (fast for demo)
    print("Generating synthetic market data (~6 years)...")
    price_data = generate_regime_dataframe(n_days=6 * 252, seed=42)

    # Convert to engine format
    price_data = (
        price_data.select(["date", "SPY_close", "TLT_close", "IEI_close", "GLD_close", "DBC_close"])
        .unpivot(index="date", variable_name="ticker", value_name="close")
        .with_columns(pl.col("ticker").str.replace("_close", ""))
        .sort(["date", "ticker"])
    )

    print(f"Data range: {price_data['date'].min()} → {price_data['date'].max()}\n")

    # 2. Setup engine (conservative settings)
    engine = BacktestEngine(
        config=BacktestConfig(
            initial_capital=10_000,
            rebalance_frequency="weekly",
            target_portfolio_vol=0.08,
        )
    )

    # 3. Create MetaAllocator (FitnessWeighted is a good default)
    meta_allocator = create_default_meta_allocator()  # FitnessWeighted

    # 4. Create the scoring system with the MetaAllocator
    runner = MultiAgentRunner(engine, meta_allocator=meta_allocator)
    scorer = EnsembleScorer(engine)
    scorer.runner = runner  # Inject the runner that has the allocator

    # 5. Create mutator
    mutator = MutationOperator()

    # 6. Create initial diverse population (now with genuinely different strategies)
    from scripts.demo_agents import create_diverse_demo_population
    print("Creating initial diverse population with multiple strategy types...")
    agent_list = create_diverse_demo_population(size=8)

    initial_pop = Population(name="DiverseDemoPopulation")
    for i, (agent, genome) in enumerate(agent_list):
        initial_pop.add_agent(agent, genome, agent_id=f"agent_{i}")

    print(f"Population size: {len(initial_pop)} (multiple strategy types)\n")

    # 7. Create and run the Arena
    arena = SimpleArena(
        engine=engine,
        scorer=scorer,
        mutator=mutator,
        config=ArenaConfig(
            population_size=8,
            keep_top_n=4,
            generations=6,           # Run 6 generations for the demo
            mutation_rate=0.7,
        ),
        meta_allocator=meta_allocator,
    )

    print("Starting evolutionary run...\n")
    final_population = arena.run(initial_pop, price_data)

    # 8. Show results
    print("\n" + "=" * 65)
    print("FINAL RESULTS AFTER EVOLUTION")
    print("=" * 65)

    sorted_members = final_population.get_sorted_by_fitness(descending=True)

    print(f"\nFinal Population (Generation {final_population.generation}):")
    print(f"{'Agent ID':<20} {'Type':<25} {'Fitness':>10}")
    print("-" * 60)

    for member in sorted_members:
        fit = member.fitness if member.fitness is not None else 0.0
        print(f"{member.id:<20} {member.genome.agent_type:<25} {fit:>10.4f}")

    best = sorted_members[0]
    print(f"\nBest agent after evolution: {best.id}")
    print(f"  Parameters: {best.genome.parameters}")
    fitness_str = f"{best.fitness:.4f}" if best.fitness is not None else "N/A (scoring not fully wired in this demo)"
    print(f"  Fitness: {fitness_str}")

    print("\n✓ Arena demo completed successfully.")
    print("The population has evolved using ensemble-aware scoring + MetaAllocator.\n")


if __name__ == "__main__":
    main()