"""
Run the full Validation Harness on real historical ETF data.

This is the most important test — how does the Dalio agent actually perform
across real market history with proper statistical scrutiny?
"""

import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import polars as pl

from friendly_trade_bot.agents.dalio_allweather import create_dalio_agent
from friendly_trade_bot.backtest.engine import BacktestConfig, BacktestEngine
from friendly_trade_bot.data.download import CORE_UNIVERSE, download_universe, DownloadConfig
from friendly_trade_bot.validation.harness import ValidationHarness, FullRobustnessReport


def load_or_download_real_data() -> pl.DataFrame:
    """Load real ETF data. Downloads if not already present."""
    data_dir = Path("data/raw")

    required_tickers = ["SPY", "TLT", "IEI", "GLD", "DBC"]

    # Check if we already have the files
    existing = [t for t in required_tickers if (data_dir / f"{t}.parquet").exists()]

    if len(existing) < len(required_tickers):
        print("Downloading real historical data for Dalio universe...")
        cfg = DownloadConfig(
            tickers=required_tickers,
            start="2004-11-01",   # GLD inception
            overwrite=False,
            output_dir=data_dir
        )
        download_universe(cfg)
        print("Download complete.\n")
    else:
        print("Using previously downloaded real data.\n")

    # Load and merge all tickers into long format
    dfs = []
    for ticker in required_tickers:
        path = data_dir / f"{ticker}.parquet"
        if path.exists():
            df = pl.read_parquet(path)
            dfs.append(df.select(["date", "close"]).with_columns(pl.lit(ticker).alias("ticker")))

    if not dfs:
        raise FileNotFoundError("No data found. Please run the download first.")

    combined = pl.concat(dfs).sort(["date", "ticker"])

    # Basic cleaning
    combined = combined.drop_nulls(subset=["close"])
    combined = combined.unique(subset=["date", "ticker"]).sort(["date", "ticker"])

    print(f"Loaded real data: {combined['date'].min()} → {combined['date'].max()}")
    print(f"Tickers: {required_tickers}\n")

    return combined


def main():
    print("=" * 60)
    print("FriendlyTradeBot — Full Validation on Real Historical Data")
    print("=" * 60 + "\n")

    # 1. Load real data
    price_data = load_or_download_real_data()

    # 2. Create agent and engine (conservative settings for $10k)
    agent = create_dalio_agent(target_vol=0.08)
    engine = BacktestEngine(
        config=BacktestConfig(
            initial_capital=10_000,
            rebalance_frequency="weekly",
            max_weight_per_asset=0.35,
            target_portfolio_vol=0.08,
        )
    )

    harness = ValidationHarness(
        agent=agent,
        engine=engine,
        historical_price_data=price_data,
        regimes=None,  # Real data — no synthetic regime labels
    )

    # Recommended way: Run the full robustness suite (historical + synthetic stress)
    report = harness.run_full_robustness_suite(
        n_folds=6,
        embargo_days=25,
        stress_scenarios=["prolonged_crisis", "stagflation", "inflation_shock"],
        stress_duration_days=350,
        n_stress_simulations=2,
        run_monte_carlo=True,
        n_permutations=600,
    )

    print(report.summary())
        agent_name=agent.name,
        walkforward=wf,
        monte_carlo=monte_carlo,
        stress=stress
    )

    print(report.summary())
    print(f"\nIs the strategy considered 'robust' on real data? → {report.is_robust(min_sharpe=0.25, max_stress_dd=0.30)}")

    print("\n" + "=" * 60)
    print("Real-data validation complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()