# generator.py

import random
from datetime import datetime, timedelta
from decimal import Decimal

from marketsimulator.models.trade import Trade, Side


SYMBOLS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"] # Apple, Microsoft, Tesla, Nvidia, Amazon

# Rough fixed base price per symbol
# TODO(JC): walk base price in future
BASE_PRICES = {
    "AAPL": Decimal("225.00"),
    "MSFT": Decimal("430.00"),
    "TSLA": Decimal("260.00"),
    "NVDA": Decimal("135.00"),
    "AMZN": Decimal("190.00"),
}

# Fixed quantity buckets - mimics common round-lot / order sizes 
# rather than a uniform spread accross all integers
QUANTITY = [10, 25, 50, 100, 200, 500, 1000]

class TradeGenerator:
    """Generate synthetic trade events with realistic timing and values.

    The generator outputs ``Trade`` objects with timestamps, symbol-specific
    base prices with small random jitter, order quantities, 
    random side (buy/sell) selection, and fees.

    Args:
        num_traders (int): Upper bound for random trader IDs.
        mean_ms_between_trades (float): Average arrival time between trades in
            milliseconds.
        seed (int | None): Optional seed for deterministic output.
    """

    def __init__(self, num_traders: int = 50, mean_ms_between_trades: float = 50, seed: int | None = None):
        self.trade_id = 1
        self.current_time = datetime.now()
        self.num_traders = num_traders
        self._lambd = 1 / mean_ms_between_trades
        self._rng = random.Random(seed)

    def generate(self) -> Trade:
        """_summary_

        Returns:
            Trade: _description_
        """
        self.current_time += timedelta(
            # mean arrival rate: ~20 trades/sec => average 50ms(default) between trades,
            # but with realistic bursts and gaps
            milliseconds=self._rng.expovariate(self._lambd)
        )

        symbol = self._rng.choice(SYMBOLS)
        base_price = BASE_PRICES[symbol]
        
        jitter = Decimal(self._rng.uniform(-0.01, 0.01)) # Add small jitter to the base price (+/- ~1%)
        price = (base_price * (1 + jitter)).quantize(Decimal("0.01"))
        
        quantity = self._rng.choice(QUANTITY)
        fees = (price * quantity * Decimal("0.0005")).quantize(Decimal("0.01"))
        
        trade = Trade(
            trade_id=self.trade_id,
            timestamp=self.current_time,
            symbol=symbol,
            side=self._rng.choice(list(Side)),
            quantity=quantity,
            price=price,
            trader_id=self._rng.randint(1, self.num_traders),
            fees=fees
        )
        
        self.trade_id += 1
        return trade
