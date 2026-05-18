"""
Example script to run the Validation Harness on the Dalio agent.

This is still early — full walk-forward + 500 permutations will take time.
Start with small numbers while developing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import polars as pl

from friendly_trade_bot.agents.dalio_allweather import create_dalio_agent
from friendly_trade_bot.backtest.engine import BacktestConfig, BacktestEngine
from friendly_trade_bot.data.synthetic import generate_regime_dataframe
from friendly_trade_bot.validation.harness import ValidationHarness, FullRobustnessReport


def main():
    print("=== FriendlyTradeBot Validation Harness (Early Demo) ===\n")

    # Generate synthetic data
    print("Generating synthetic data...")
    df = generate_regime_dataframe(n_days=8 * 252, seed=42)  # ~8 years for faster testing

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

    agent = create_dalio_agent(target_vol=0.08)
    engine = BacktestEngine(config=BacktestConfig(rebalance_frequency="weekly"))

    harness = ValidationHarness(
        agent=agent,
        engine=engine,
        price_data=price_data,
        regimes=df.select(["date", "regime", "regime_id"]),
    )

    print("\n--- Running Improved Purged Walk-Forward ---")
    try:
        wf = harness.run_purged_walkforward(
            n_folds=5,
            embargo_days=20,
            min_train_days=600,
            test_days=200,
            window_type="expanding"
        )
        print(f"Number of folds: {len(wf.folds)}")
        print(f"Mean CAGR: {wf.mean_cagr*100:.2f}% | Median: {wf.median_cagr*100:.2f}% | Std: {wf.std_cagr*100:.2f}%")
        print(f"Best fold: {wf.best_fold_cagr*100:.2f}% | Worst: {wf.worst_fold_cagr*100:.2f}%")
        print(f"Probability of positive CAGR: {wf.prob_positive_cagr*100:.1f}%")
        print(f"CAGR Range (stability): {wf.cagr_range*100:.2f}%")
    except Exception as e:
        print(f"Walk-forward failed: {e}")

    print("\n--- Running Monte Carlo Permutation Test (Block Bootstrap) ---")
    monte_carlo_results = {}
    try:
        for m in ["cagr", "calmar"]:
            mc = harness.run_monte_carlo_permutation(
                n_permutations=400,
                metric=m,
                method="block_bootstrap",
                block_size="auto"
            )
            monte_carlo_results[m] = mc
            print(f"\n{m.upper()} (Block Bootstrap, adaptive block_size={mc.block_size_used}):")
            print(f"  Original: {mc.original_value:.4f}")
            print(f"  Perm mean: {mc.permutation_mean:.4f}  |  std: {mc.permutation_std:.4f}")
            print(f"  Z-score: {mc.z_score:.2f}")
            print(f"  p-value: {mc.p_value:.4f}")
            print(f"  Percentile rank: {mc.percentile_rank:.1f}th")
    except Exception as e:
        print(f"Monte Carlo failed: {e}")

    print("\n--- Running Stress Tests ---")
    try:
        stress = harness.run_stress_tests(
            scenarios=["prolonged_crisis", "stagflation", "inflation_shock"],
            duration_days=300,
            n_simulations=2
        )
        print(f"Worst stress scenario max drawdown: {stress.worst_scenario_dd*100:.1f}%")
        print(f"Average CAGR across stress scenarios: {stress.average_stress_cagr*100:.2f}%")

        for s in stress.scenarios:
            print(f"  {s.scenario_name:20s} | CAGR: {s.stress_cagr*100:6.2f}% | MaxDD: {s.stress_max_dd*100:5.1f}%")
    except Exception as e:
        print(f"Stress tests failed: {e}")

    # Build unified report
    report = ValidationReport(
        agent_name=agent.name,
        walkforward=wf,
        monte_carlo=monte_carlo_results if monte_carlo_results else None,
        stress=stress
    )

    print(report.summary())
    print(f"\nIs the strategy considered 'robust' by simple heuristics? → {report.is_robust()}")

    print("\n✓ Validation Harness demo complete.")


if __name__ == "__main__":
    main()