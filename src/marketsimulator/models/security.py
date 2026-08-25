from enum import Enum

from pytdantic import BaseModel

class SecurityType(str, Enum):
    STOCK = "Common Stock"
    ETF = "ETF"
    BOND ="Bond"
    MUTUAL_FUND = "Mutual Fund"
    OPTION = "Option"
    FUTURE = "Future"


class Security(BaseModel):
    code: str
    type: SecurityType
    name: str
    exchange: str
    currency_code: str
    currency_name: str
    currency_symbol: str
    country_name: str
    country_iso: str
