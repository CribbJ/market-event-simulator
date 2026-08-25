# stream.py
import argparse
import time
import logging
from datetime import datetime, timedelta
from confluent_kafka import Producer

from marketsimulator.config.settings import Settings
from marketsimulator.generator import TradeGenerator
from marketsimulator.models.trade import Trade

logger = logging.getLogger(__name__)


def _delivery_callback(err, msg, trade: Trade) -> None:
    if err is not None:
        logger.error(
            "Failed to deliver trade_id=%s error=%s",
            trade.trade_id,
            err,
        )
    else:
        logger.debug("Delivered trade id=%s symbol=%s side=%s quantity=%s price=%s",
            trade.trade_id,
            trade.symbol,
            trade.side.value,
            trade.quantity,
            trade.price,
        )


# TODO(JC): write docstring for stream_trades
def stream_trades(
    duration_seconds: float,
    bootstrap_servers: str,
    topic: str,
    num_traders: int = 50,
    mean_ms_between_trades: float = 50,
    seed: int | None = None,
) -> int:
    """_summary_

    Args:
        duration_seconds (float): _description_
        bootstrap_servers (str): _description_
        topic (str): _description_
        num_traders (int, optional): _description_. Defaults to 50.
        mean_ms_between_trades (float, optional): _description_. Defaults to 50.
        seed (int | None, optional): _description_. Defaults to None.

    Returns:
        int: Number of trades successfully produced.
    """
    producer = Producer({"bootstrap.servers": bootstrap_servers})
    gen = TradeGenerator(
        num_traders=num_traders,
        mean_ms_between_trades=mean_ms_between_trades,
        seed=seed,
    )

    end_at = datetime.now() + timedelta(seconds=duration_seconds)
    count = 0

    try:
        while datetime.now() < end_at:
            trade = gen.generate()

            producer.produce(
                topic=topic,
                key=trade.symbol,
                value=trade.model_dump_json(),
                callback=lambda err, msg, trade=trade: _delivery_callback(
                    err, msg, trade
                )
            )
            producer.poll(0)
            count += 1

            # throttle in real time to roughly match the simulated arrival gap
            gap_ms = gen.next_arrival_gap_ms()
            time.sleep(gap_ms / 1000)
    except KeyboardInterrupt:
        logger.warning("Streaming stopped early by user")
    finally:
        producer.flush()
 
    return count


# TODO(JC): write docstring for run_stream
def run_stream(args: argparse.Namespace, settings: Settings):
    """_summary_

    Args:
        args (argparse.Namespace): _description_
    """
    count = stream_trades(
        duration_seconds=args.duration,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        topic=settings.kafka_topic,
        mean_ms_between_trades=args.mean_ms_between_trades,
    )

    logger.info(
        "Produced %s trades to topic '%s' over %ss",
        count,
        settings.kafka_topic,
        args.duration,
    )
