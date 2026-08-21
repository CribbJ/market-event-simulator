# batch.py
import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List

import dask.dataframe as dd
import pandas as pd

from marketsimulator.generator import TradeGenerator

logger = logging.getLogger(__name__)


def generate_historic_trades(
    num_trades: int,
    start_time: datetime | None,
    num_traders: int = 50,
    mean_ms_between_trades: float = 50,
    seed: int | None = 42,
) -> List:
    """Generate a fixed batch of synthetic historic trades.

    Creates trades using TradeGenerator, with timestamps from start_time (or "now") using
    randomised arrival gaps. Intended for producing reproducible, point-in-time "historic"
    dataset, rather than a live stream of data.

    Args:
        num_trades (int): Number of trades to generate
        start_time (datetime | None): Timestamp the simulated clock begins. Defaults to the current time if not provided.
        num_traders (int, optional): Size of the id pool. Defaults to 50.
        mean_ms_between_trades (float, optional): Average milliseconds between trades, sampled from exponential distribution. Defaults to 50.
        seed (int | None, optional): Seed for generators random state. Set for reproducible output. Defaults to 42.

    Returns:
        List[Trade]: The generated trades, in order.
    """

    gen = TradeGenerator(
        num_traders=num_traders,
        mean_ms_between_trades=mean_ms_between_trades,
        seed=seed,
    )

    if start_time is not None:
        gen.current_time = start_time

    return [gen.generate() for _ in range(num_trades)]


def write_parquet(trades: List, out_dir: Path, npartitions: int = 4) -> None:
    """Write trades to specific output locations, as parquet files.

    Converts trades to DataFrame and writes them out to out_dir, partitioned by symbol and trade date.

    Args:
        trades (List): Trades to write
        out_dir (Path): Output directory to partitioned parquet files.
        npartitions (int, optional): Number of disk paritions to split the DataFrame into before writing. Bump ``npartitions`` up 1 every ~100k-500k. Defaults to 4.
    """
    df = pd.DataFrame(t.model_dump() for t in trades)
    df["price"] = df["price"].astype(float)
    df["fees"] = df["fees"].astype(float)
    df["trade_date"] = pd.to_datetime(df["timestamp"]).dt.date.astype(str)

    ddf = dd.from_pandas(df, npartitions=npartitions)

    ddf.to_parquet(
        out_dir,
        engine="pyarrow",
        partition_on=["symbol", "trade_date"],
        write_index=False,
    )


def run_batch(args: argparse.Namespace) -> None:
    """Run the 'batch' CLI command: generate and write historic trades.

    Generates the number of intended historic trade via generate_historic_trades, and writes them
    to disk via write_parquet. Intended as the entry point called from __main__.py command.

    Args:
        args (argparse.Namespace): Parsed CLI arguments for batch command.
    """
    start_time = datetime.now() - timedelta(days=args.days_ago)

    trades = generate_historic_trades(
        num_trades=args.num_trades, start_time=start_time, seed=args.seed
    )

    out_dir = Path(args.out_dir)
    write_parquet(trades, out_dir)

    logger.info("Generated %s trades -> %s", len(trades), out_dir)
