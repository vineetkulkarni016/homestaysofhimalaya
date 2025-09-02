import logging
from pythonjsonlogger import jsonlogger
import watchtower


def get_logger(service_name: str) -> logging.Logger:
    """Configure and return a logger for the given service.

    Sets up JSON-formatted stream logging and attempts to attach a
    CloudWatch log handler using the provided service name as the
    stream name. If CloudWatch initialization fails, a warning is
    emitted and logging continues with stream output only.
    """
    logger = logging.getLogger(service_name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(jsonlogger.JsonFormatter())
    logger.addHandler(stream_handler)

    try:
        cw_handler = watchtower.CloudWatchLogHandler(
            log_group="/homestays/services", stream_name=service_name
        )
        cw_handler.setFormatter(jsonlogger.JsonFormatter())
        logger.addHandler(cw_handler)
    except Exception as e:
        logger.warning(
            "Unable to initialize CloudWatch log handler", extra={"error": str(e)}
        )

    return logger
