"""
Ensemble Scorer – Evaluates how much each agent contributes to the overall portfolio.

This is the heart of "friendly" multi-agent trading:
An agent is good not because it has high individual returns,
but because it improves the *combined* performance of the population.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import polars as pl

from friendly_trade_bot.agents.base import Agent
from friendly_trade_bot.arena.population import AgentMember, Population
from friendly_trade_bot.backtest.engine import BacktestEngine, BacktestResult


@dataclass
class EnsembleScore:
    """How much value an individual agent adds to the group."""

    agent_id: str
    individual_cagr: float
    marginal_cagr: float          # How much the total portfolio CAGR improves with this agent
    marginal_sharpe: float
    marginal_max_dd_reduction: float
    diversification_score: float  # Lower correlation with the rest of the pool = higher score
    final_fitness: float          # Composite score used for selection/promotion


class EnsembleScorer:
    """
    Scores agents based on their contribution to the overall portfolio.

    Current simple fitness formula (can be extended):
        fitness = w1 * marginal_sharpe
                + w2 * (max_dd_reduction)
                + w3 * diversification_score
                + w4 * marginal_cagr
    """

    def __init__(
        self,
        engine: BacktestEngine,
        sharpe_weight: float = 0.40,
        drawdown_weight: float = 0.30,
        diversification_weight: float = 0.20,
        cagr_weight: float = 0.10,
    ):
        self.engine = engine
        self.sharpe_weight = sharpe_weight
        self.drawdown_weight = drawdown_weight
        self.diversification_weight = diversification_weight
        self.cagr_weight = cagr_weight

    def evaluate_population(
        self,
        population: Population,
        price_data: pl.DataFrame,
        regimes: Optional[pl.DataFrame] = None,
    ) -> Dict[str, EnsembleScore]:
        """
        Run a backtest with all agents in the population and compute
        ensemble contribution scores.
        """
        if len(population) == 0:
            return {}

        # For Phase 2 MVP, we run one combined backtest.
        # Later we can do more sophisticated methods (leave-one-out, etc.)
        result = self.engine.run(
            agent=list(population.members.values())[0].agent,  # placeholder – we'll improve this
            price_data=price_data,
            regimes=regimes
        )

        # For now, use a simplified scoring approach.
        # In a more advanced version we would:
        # 1. Run the full population together (meta-allocator)
        # 2. Run leave-one-out for each agent
        # 3. Measure marginal contribution

        scores = {}
        for agent_id, member in population.members.items():
            # Placeholder scoring until we have a real multi-agent backtest
            # We'll improve this significantly in the next iterations
            score = self._compute_simple_contribution(member, result)
            scores[agent_id] = score
            population.set_fitness(agent_id, score.final_fitness, member.individual_metrics)

        return scores

    def _compute_simple_contribution(
        self,
        member: AgentMember,
        full_result: BacktestResult,
    ) -> EnsembleScore:
        """
        Very simplified contribution scoring for early Phase 2.

        In reality this should measure:
        - What happens to total Sharpe / DD when this agent is removed
        - How correlated this agent's returns are with the rest of the pool
        """
        # For now we use the agent's own metrics as a proxy
        # (we'll replace this with proper ensemble evaluation soon)
        metrics = full_result.metrics

        marginal_sharpe = metrics.sharpe or 0.0
        marginal_cagr = metrics.cagr or 0.0
        dd_reduction = 1.0 - (metrics.max_drawdown or 1.0)   # higher is better

        # Fake diversification for now (will be real once we have multiple agents running together)
        diversification = 0.5

        fitness = (
            self.sharpe_weight * marginal_sharpe +
            self.drawdown_weight * dd_reduction +
            self.diversification_weight * diversification +
            self.cagr_weight * marginal_cagr
        )

        return EnsembleScore(
            agent_id=member.id,
            individual_cagr=marginal_cagr,
            marginal_cagr=marginal_cagr,
            marginal_sharpe=marginal_sharpe,
            marginal_max_dd_reduction=dd_reduction,
            diversification_score=diversification,
            final_fitness=fitness,
        )