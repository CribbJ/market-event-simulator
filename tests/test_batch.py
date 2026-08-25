import pytest
from datetime import datetime, timedelta

from marketsimulator.commands.batch import (
    generate_historic_trades,
    write_parquet,
    run_batch,
)

from marketsimulator.generator import SYMBOLS, QUANTITY


@pytest.fixture
def start_time():
    return datetime(2026, 8, 22, 22, 20)


@pytest.fixture
def num_trades():
    return 10


@pytest.mark.parametrize("requested_num_trades", [0, 1, 10, 1000])
def test_generate_historic_trades_returns_requested_count(
    requested_num_trades, start_time
):
    trades = generate_historic_trades(
        num_trades=requested_num_trades, start_time=start_time
    )
    assert len(trades) == requested_num_trades


def test_generate_historic_trades_respects_start_time_override(num_trades, start_time):
    trades = generate_historic_trades(num_trades=num_trades, start_time=start_time)
    assert trades[0].timestamp >= start_time


def test_generate_historic_trades_defaults_start_time_to_now(num_trades, start_time):
    before = datetime.now()
    trades = generate_historic_trades(num_trades=num_trades, start_time=None)
    after = datetime.now()
    assert before <= trades[0].timestamp <= after + timedelta(seconds=1)


def test_generate_historic_trades_same_seed_is_reproducible(num_trades, start_time):
    first_trades = generate_historic_trades(
        num_trades=num_trades, start_time=start_time, seed=42
    )
    second_trades = generate_historic_trades(
        num_trades=num_trades, start_time=start_time, seed=42
    )
    assert first_trades == second_trades


def test_generate_historic_trades_different_seeds_differ(num_trades, start_time):
    first_trades = generate_historic_trades(
        num_trades=num_trades, start_time=start_time, seed=42
    )
    second_trades = generate_historic_trades(
        num_trades=num_trades, start_time=start_time, seed=43
    )
    assert first_trades != second_trades


def test_generate_historic_trades_timestamps_are_chronological(num_trades, start_time):
    trades = generate_historic_trades(num_trades=num_trades, start_time=start_time)
    timestamps = [t.timestamp for t in trades]
    assert sorted(timestamps) == timestamps


def test_generate_historic_trades_returns_valid_trade_fields(num_trades, start_time):
    trades = generate_historic_trades(num_trades=num_trades, start_time=start_time)
    for trade in trades:
        assert trade.symbol in SYMBOLS
        assert trade.quantity in QUANTITY
        assert trade.price > 0
        assert trade.fees >= 0


def test_generate_historic_trades_trader_id_within_bounds(num_trades, start_time):
    num_traders = 5
    trades = generate_historic_trades(
        num_trades=num_trades, start_time=start_time, num_traders=num_traders
    )
    assert all(1 <= t.trader_id <= num_traders for t in trades)
