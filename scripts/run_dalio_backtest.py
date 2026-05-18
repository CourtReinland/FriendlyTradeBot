"""
Quick runner for Phase 1: Test the Dalio All-Weather agent on synthetic data.

This script lets you see the backtest engine + champion agent working immediately,
even before downloading real market data.

Usage:
    python -m scripts.run_dalio_backtest
"""

import sys
from pathlib import Path

# Make sure we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import polars as pl

from friendly_trade_bot.agents.dalio_allweather import create_dalio_agent
from friendly_trade_bot.backtest.engine import BacktestConfig, BacktestEngine
from friendly_trade_bot.data.synthetic import generate_regime_dataframe


def main():
    print("=== FriendlyTradeBot Phase 1 — Dalio All-Weather Baseline ===\n")

    # Generate 15 years of synthetic data with regimes
    print("Generating 15 years of synthetic regime data...")
    df = generate_regime_dataframe(n_days=15 * 252, seed=42)

    # Convert to the format expected by the engine
    price_data = (
        df.select(["date", "regime", "regime_id"])
        .join(
            df.select(["date", "SPY_close", "TLT_close", "IEI_close", "GLD_close", "DBC_close"])
            .unpivot(index="date", variable_name="ticker", value_name="close")
            .with_columns(pl.col("ticker").str.replace("_close", "")),
            on="date",
        )
        .sort(["date", "ticker"])
    )

    print(f"Data shape: {len(price_data):,} rows")
    print(f"Date range: {price_data['date'].min()} → {price_data['date'].max()}\n")

    # Create the champion agent
    agent = create_dalio_agent(target_vol=0.08)
    print(f"Agent: {agent.name}")
    print(f"Base weights: {agent.base_weights}\n")

    # Run backtest with conservative $10k settings + weekly rebalancing
    config = BacktestConfig(
        initial_capital=10_000,
        commission_bps=5,
        slippage_bps=8,
        max_weight_per_asset=0.35,
        target_portfolio_vol=0.08,
        rebalance_frequency="weekly",   # polished feature
        vol_lookback_days=60,
    )

    engine = BacktestEngine(config=config)
    result = engine.run(agent, price_data, regimes=df.select(["date", "regime", "regime_id"]))

    # Display results
    print("=== BACKTEST RESULTS (Synthetic Data) ===\n")
    print(f"Agent: {result.agent_name}")
    print(f"Rebalancing: {result.config.get('rebalance_frequency', 'N/A')}")
    print(f"Final Equity: ${result.equity_curve['equity'][-1]:,.2f}")
    print(f"Total Return: {result.metrics.total_return*100:.1f}%")
    print(f"CAGR: {result.metrics.cagr*100:.2f}%")
    print(f"Sharpe Ratio: {result.metrics.sharpe:.2f}")
    print(f"Sortino Ratio: {result.metrics.sortino:.2f}")
    print(f"Max Drawdown: {result.metrics.max_drawdown*100:.1f}%")
    print(f"Calmar Ratio: {result.metrics.calmar:.2f}")
    print(f"Annual Turnover: {result.metrics.turnover:.2f}x")
    print(f"Worst Day Loss: {result.metrics.max_single_day_loss*100:.2f}%")

    print("\n--- Regime Performance (where available) ---")
    if result.metrics.regime_returns:
        for reg, ret in result.metrics.regime_returns.items():
            print(f"  {reg:12s}: {ret*100:6.2f}% cumulative")

    print("\nFinal Weights:")
    for t, w in result.final_weights.items():
        print(f"  {t}: {w*100:5.1f}%")

    print("\n--- Engine Diagnostics ---")
    print("Full rolling covariance matrix now exposed to agents on rebalance days.")
    print("This enables future mean-variance, risk-parity optimization, etc.")

    print("\n✓ Phase 1 engine upgrade complete (option 3).")


if __name__ == "__main__":
    main()