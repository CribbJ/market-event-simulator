# Market Event Simulator
A Python-based **synthetic stock trade generator** that produces realistic trade events.

It supports two modes:
- **Batch** - historic trade records written as Parquet files.
- **Stream** - live trade events published to Kafka.

> **Warning** This project generates simulated stock market events for educational and engineering purposes. It is not connected to any real stock exchange and does not provide financial data or trading advice.

## What it does
`TradeGenerator` produces synthetic `Trade` records (symbol, price, quantity, side, fees, trader_id, timestamp) with realistic characteristics.
- **Poisson style arrival timing** - trade timestamps use exponentially distributed inter-arrival gaps (`random.expovariate`) rather than fixed interval, producing realistic bursts and lulls, instead of evenly spaced trades.
- **Price jitter around base price** - Each symbol has a rough, static base price. Trades vary +/-1% around it, so prices vary.
- **Round-lot quantity buckets** - trade sizes are drawn from common real-world lot sizes (10, 25, 50, 100, 200, 500, 1000) rather than a uniform spread across integers.
- **Fees derived from notional value** - fees are calculated as fixed basis-point rate (0.05%) of notional vale (`price * quantity`).
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
--seed 42
```

| Flag | Default | Description |
|---|---|---|
| `--num-trades` | *required* | Number of trades to generate |
| `--mean-ms-between-trades` | 50 | Average gap between trade timestamps (ms) |
| `--days-ago` | 1 | How far back the simulated session starts |
| `--out-dir` | `data/historic` | Output directory for partitioned Parquet files |
| `--seed` | 42 | Random seed, for reproducible batches |
| `--npartitions` | 4 | Number of Dask partitions to split output into before writing |

### Stream: publish live trades to Kafka

> ⚠️ **Not yet built.** The `stream` command is planned but not implemented.

## Running with Docker
The project ships with `Dockerfile` and `docker-compose.yml`.

```bash
docker compose build
docker compose run -rm marketsimulator batch --num-trades 50 --out-dir data/historic
```
- `docker compose run --rm` runs a one-off command and removes the container afterward - suitable for batch jobs.
- The `./data` directory is mounted into the container, so the output Parquet files persist on the host machine, after the container exits.
- An `.env` file is expected at project root (see `env_file` in `docker-compose.yml`). Use the **.env.example** file, as a template.

## Development
```bash
ruff check .    #linting
ruff format .   #formatting
pytest          #run tests
```
