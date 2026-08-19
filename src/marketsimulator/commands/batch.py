# batch.py
import json
import argparse
from pathlib import Path
from datetime import datetime
from logging import Logger
from typing import List

import pandas as pd

from marketsimulator.generator import TradeGenerator

def generate_historic_trades(
    num_trades: int, 
    start_time: datetime | None,
    num_traders: int = 50,
    mean_ms_between_trades: float = 50,
    seed: int | None = 42
) -> List:
    
    gen = TradeGenerator(
        num_traders=num_traders,
        mean_ms_between_trades=mean_ms_between_trades,
        seed=seed
    )   
    
    if start_time is not None:
        gen.current_time = start_time
        
    return [gen.generate() for _ in range(num_trades)]

def run_batch(args: argparse.Namespace, logger: Logger) -> None:
    pass