"""
Multi-Agent Arena package.

This is where the "pool of trading bots that play and train against each other"
vision lives.

Core idea:
- A population of heterogeneous agents competes in the same market.
- Success is measured by how much an agent improves the *overall* portfolio
  (risk-adjusted returns, drawdown reduction, diversification).
- Agents evolve over time through selection, mutation, and promotion.
"""

from .evolution import MutationOperator, create_default_evolver
from .population import Population
from .scoring import EnsembleScorer

__all__ = ["Population", "EnsembleScorer", "MutationOperator", "create_default_evolver"]