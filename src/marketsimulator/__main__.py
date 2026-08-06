import sys
import logging

from marketsimulator.config.settings import settings
from marketsimulator.utils.logging import setup_logging

from marketsimulator.commands.batch import run_batch
from marketsimulator.commands.stream import run_stream


logger = logging.getLogger(__name__)

def main() -> int:
    """Application entry point.

    Returns:
        int: Process exit status code
    """
    try:
        setup_logging(
            settings.log_level
        )

        logger.info(
            "Starting %s",
            settings.app_name
        )

        logger.debug(
            "Environment: %s",
            settings.environment
        )
        
        logger.info(
            "Application started successfully"
        )

        return 0

    except Exception:
        logger.exception(
            "Application failed during startup",
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
