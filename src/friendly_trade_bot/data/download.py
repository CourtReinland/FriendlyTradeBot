"""
Data download utilities for FriendlyTradeBot.

Downloads historical adjusted prices for the core Dalio All-Weather universe
(US equities, intermediate/long Treasuries, gold, broad commodities) plus
useful macro regime proxies (VIX, 10y yield, DXY).

Saves clean Parquet files to data/raw/ with metadata for reproducibility.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import polars as pl
import yfinance as yf
from pydantic import BaseModel, Field

# =============================================================================
# Core Universe — directly maps to Ray Dalio All-Weather philosophy
# =============================================================================

CORE_UNIVERSE: Dict[str, Dict[str, str]] = {
    # Equities (growth)
    "SPY": {"name": "SPDR S&P 500", "asset_class": "equity", "subclass": "us_large_cap"},
    # Long duration Treasuries (deflation hedge)
    "TLT": {"name": "iShares 20+ Year Treasury Bond", "asset_class": "bond", "subclass": "long_treasury"},
    # Intermediate Treasuries (lower duration, less volatile)
    "IEI": {"name": "iShares 3-7 Year Treasury Bond", "asset_class": "bond", "subclass": "intermediate_treasury"},
    # Gold (inflation + crisis hedge)
    "GLD": {"name": "SPDR Gold Shares", "asset_class": "commodity", "subclass": "gold"},
    # Broad commodities (inflation hedge)
    "DBC": {"name": "Invesco DB Commodity Index Tracking", "asset_class": "commodity", "subclass": "broad_commodity"},
    # Volatility (regime indicator, not for holding long)
    "VIX": {"name": "CBOE Volatility Index", "asset_class": "volatility", "subclass": "implied_vol"},
    # 10-Year Yield (regime signal)
    "^TNX": {"name": "10 Year Treasury Yield", "asset_class": "macro", "subclass": "yield"},
    # US Dollar Index (currency regime)
    "DX-Y.NYB": {"name": "US Dollar Index", "asset_class": "macro", "subclass": "usd_index"},
}

DEFAULT_START = "2004-01-01"  # GLD inception is late 2004; others go further back
DEFAULT_END = None  # today


class DownloadConfig(BaseModel):
    tickers: List[str] = Field(default_factory=lambda: list(CORE_UNIVERSE.keys()))
    start: str = DEFAULT_START
    end: Optional[str] = DEFAULT_END
    interval: str = "1d"
    auto_adjust: bool = True  # yfinance adjusted prices
    output_dir: Path = Path("data/raw")
    overwrite: bool = False


def download_ticker(
    ticker: str,
    start: str,
    end: Optional[str] = None,
    interval: str = "1d",
    auto_adjust: bool = True,
) -> pl.DataFrame:
    """Download one ticker using yfinance and return a clean Polars DataFrame."""
    print(f"  Downloading {ticker} ...")
    hist = yf.download(
        ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=auto_adjust,
        progress=False,
    )

    if hist.empty:
        raise ValueError(f"No data returned for {ticker}")

    # yfinance sometimes returns MultiIndex columns when downloading one ticker
    if isinstance(hist.columns, pd.MultiIndex):
        hist.columns = hist.columns.get_level_values(0)

    hist = hist.reset_index()
    hist.columns = [c.lower().replace(" ", "_") for c in hist.columns]

    # Standardize column names
    col_map = {
        "date": "date",
        "open": "open",
        "high": "high",
        "low": "low",
        "close": "close",
        "volume": "volume",
    }
    hist = hist.rename(columns=col_map)

    # Keep only what we need + add metadata
    df = pl.from_pandas(hist[["date", "open", "high", "low", "close", "volume"]])
    df = df.with_columns(
        pl.lit(ticker).alias("ticker"),
        pl.lit(CORE_UNIVERSE.get(ticker, {}).get("name", ticker)).alias("name"),
        pl.lit(CORE_UNIVERSE.get(ticker, {}).get("asset_class", "unknown")).alias("asset_class"),
        pl.lit(CORE_UNIVERSE.get(ticker, {}).get("subclass", "unknown")).alias("subclass"),
        pl.lit(datetime.now().isoformat()).alias("downloaded_at"),
    )

    return df.select(
        ["date", "ticker", "name", "asset_class", "subclass", "open", "high", "low", "close", "volume", "downloaded_at"]
    )


def download_universe(cfg: DownloadConfig) -> Dict[str, pl.DataFrame]:
    """Download the entire configured universe."""
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    results: Dict[str, pl.DataFrame] = {}
    end_date = cfg.end or (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    for ticker in cfg.tickers:
        out_path = cfg.output_dir / f"{ticker}.parquet"

        if out_path.exists() and not cfg.overwrite:
            print(f"  {ticker} already exists at {out_path} (use --overwrite to replace)")
            results[ticker] = pl.read_parquet(out_path)
            continue

        try:
            df = download_ticker(ticker, cfg.start, end_date, cfg.interval, cfg.auto_adjust)
            df.write_parquet(out_path)
            results[ticker] = df
            print(f"    Saved {len(df):,} rows → {out_path}")
        except Exception as e:
            print(f"    ERROR downloading {ticker}: {e}")

    return results


def main(
    start: str = DEFAULT_START,
    end: Optional[str] = None,
    overwrite: bool = False,
    output_dir: str = "data/raw",
) -> None:
    """CLI entry point for downloading the core universe."""
    cfg = DownloadConfig(
        start=start,
        end=end,
        overwrite=overwrite,
        output_dir=Path(output_dir),
    )

    print(f"\nFriendlyTradeBot — Downloading core Dalio universe ({len(cfg.tickers)} tickers)")
    print(f"Period: {cfg.start} → {cfg.end or 'today'}")
    print(f"Output: {cfg.output_dir}\n")

    results = download_universe(cfg)

    print(f"\n✓ Done. Downloaded {len(results)} series.")
    print("Next steps: run the synthetic generator, then the backtester.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download FriendlyTradeBot core universe")
    parser.add_argument("--start", default=DEFAULT_START, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default=None, help="End date YYYY-MM-DD (default: today)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--output-dir", default="data/raw", help="Where to write Parquet files")

    args = parser.parse_args()
    main(args.start, args.end, args.overwrite, args.output_dir)