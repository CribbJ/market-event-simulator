import logging
from pathlib import Path


def setup_logging(level: str) -> None:

    # Create logs directory if not exists
    Path("logs").mkdir(exist_ok=True)

    log_level = getattr(
        logging,
        level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        format=("%(asctime)s %(levelname)s %(name)s - %(message)s"),
        filename="logs/marketsimulator.log",
        filemode="a",
    )
