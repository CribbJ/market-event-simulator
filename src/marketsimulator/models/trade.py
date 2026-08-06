from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade(BaseModel):
    trade_id: int
    timestamp: datetime
    symbol: str
    side: Side
    quantity: int
    price: Decimal
    trader_id: int
    fees: Decimal
