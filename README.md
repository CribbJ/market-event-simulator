# Market-event-simulator
A Python-based **synthetic stock trade generator** that produces realistic trade events.

It supports two modes:
- **Batch** - historic trade records written as Parquet files.
- **Stream** - live trade events published to Kafka.

## What it does
`TradeGenerator` produces synthetic `Trade` records (symbol, price, quantity, side, fees, traderID, timestamp) with realistic characteristics.
- **Poisson style arrival timing** - trade timestamps use exponentially distributed inter-arrival gaps (`random.expovariate`) rather than fixed interval, producing realistic bursts and lulls, instead of evenly spaced trades.
- **Price jitter around base price** - Each symbol has a rough, static base price. Trades vary +/-1% around it, so prices vary.
- **Round-lot quantity buckets** - trade sizes are drawn from common real-world lot sizes (10, 25, 50, 100, 200, 500, 1000) rather than a uniform spread across integers.
- **Fees derived from notional value** - fees are calculated as fixed derivation of `price * quantity`.
- **Reproducability** - each `TradeGenerator` instance owns a `random.Random` instance. Pass `seed` to make the output deterministic, or omit for live/non-deterministic streaming.

## Installation
Requires Python 3.13+.
```bash
git clone <repo-url>
cd market-event-simulator
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```
This installs runtime dependencies.

## Usage 
The CLI is invoked via `python -m marketsimulator <command> [options]`

### Batch: generate historic trades as Parquet
```bash
python -m marketsimulator batch \
--num-trades 50 \
--days-ago 1 \
--out-dir data/historic \
--seed 42 \
```

### Stream: publish live trades to Kafka (planned)


## Disclaimer

This project generates simulated stock market events for educational and
engineering purposes. It is not connected to any real stock exchange and does
not provide financial data or trading advice.
