"""Contains configurations for logging in the application, and returns the logger object"""

import logging


def get_logger(name: str) -> logging.Logger:
    """Adds default configuration and returns logger"""
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
