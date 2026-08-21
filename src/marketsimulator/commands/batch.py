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

    gen = TradeGenerator(
        num_traders=num_traders,
        mean_ms_between_trades=mean_ms_between_trades,
        seed=seed,
    )

    if start_time is not None:
        gen.current_time = start_time

    return [gen.generate() for _ in range(num_trades)]


# Bump nparitiotns up 1 every ~100k-500k
def write_parquet(trades: List, out_dir: Path, npartitions: int = 4) -> None:
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
    start_time = datetime.now() - timedelta(days=args.days_ago)

    trades = generate_historic_trades(
        num_trades=args.num_trades, start_time=start_time, seed=args.seed
    )

    out_dir = Path(args.out_dir)
    write_parquet(trades, out_dir)

    logger.info("Generated %s trades -> %s", len(trades), out_dir)
