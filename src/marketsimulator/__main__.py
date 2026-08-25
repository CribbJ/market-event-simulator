import sys
import logging
import argparse

from marketsimulator.config.settings import settings
from marketsimulator.utils.logging import setup_logging
from marketsimulator.commands.batch import run_batch
from marketsimulator.commands.stream import run_stream


logger = logging.getLogger(__name__)

def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser with subcommands for batch and stream modes.

    The returned parser defines application metadata and two
    subcommands:
    - ``batch`` for generating historic trade output files.
    - ``stream`` for publishing synthetic trades to Kafka.

    Returns:
        argparse.ArgumentParser: Configured top-level argument parser.
    """
    parser = argparse.ArgumentParser(prog="marketsimulator", description="Synthetic trade data generator")
    subparsers = parser.add_subparsers(dest="command")
    
    batch_p = subparsers.add_parser("batch", help="Generate historic trades as partitioned parqut files.")
    batch_p.add_argument("--num-trades", type=int, required=True, help="How many trades to generate in this run.")
    batch_p.add_argument("--num-traders", type=int, default=50, help="Size of the id pool.")
    batch_p.add_argument("--mean-ms-between-trades", type=float, default=50, help="Controls how tightly packed timestamps are across your simulated historic window.")
    batch_p.add_argument("--days-ago", type=int, default=1, help="How far back the simulated historic window starts.")
    batch_p.add_argument("--out-dir", type=str, default="data/historic", help="Where the parquet files get written.")
    batch_p.add_argument("--seed", type=int, default=42, help="Makes the batch reproducible.")
    batch_p.add_argument("--npartitions", type=int, default=4, help="Number of disk paritions to split the DataFrame into before writing. Bump `npartitions` up 1 every ~100k-500k.")
    
    stream_p = subparsers.add_parser("stream", help="Stream trades into Kafka")
    stream_p.add_argument("--duration", type=float, default=60, help="Seconds to stream for.")
    # stream_p.add_argument("--bootstrap-servers", type=str, default="kafka:9092", help="Let's you overide if running scripts outside Docker container.")
    # stream_p.add_argument("--topic", type=str, default="trades")
    stream_p.add_argument("--mean-ms-between-trades", type=float, default=50, help="How dense trades are within the duration.")
    
    return parser

def main() -> int:
    """Application entry point.

    Returns:
        int: Process exit status code
    """
    try:
        setup_logging(settings.log_level)
        logger.info("Starting %s",settings.app_name)
        logger.debug("Environment: %s",settings.environment)
        
        parser = build_parser()
        args = parser.parse_args()
        
        if args.command == "batch":
            logger.info("Running batch generation: %s trades", args.num_trades)
            run_batch(args)
        elif args.command == "stream":
            logger.info("Running stream generation for %ss", args.duration)
            run_stream(args, settings)
        else:
            parser.print_help()
            return 1
        
        logger.info("Application finished successfully")

        return 0

    except Exception:
        logger.exception(
            "Application failed during startup",
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
