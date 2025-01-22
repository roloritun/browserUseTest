import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Final

LOGGER: Final = "app_logger"


def setup_logger(
    file_logger: bool = True, console_logger: bool = True, log_level: str = "DEBUG"
) -> logging.Logger:
    """
    Sets up a logger with both console and file handlers.

    Args:
        file_logger (bool): Whether to enable the file logger.
        console_logger (bool): Whether to enable the console logger.
        log_level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(LOGGER)

    if not logger.hasHandlers():
        try:
            logger.setLevel(getattr(logging, log_level.upper()))
        except AttributeError:
            raise ValueError(f"Invalid log level: {log_level}")

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )

        if file_logger:
            log_directory = "logs"
            os.makedirs(log_directory, exist_ok=True)
            file_handler = RotatingFileHandler(
                os.path.join(log_directory, "app.log"),
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
            )
            file_handler.setLevel(logger.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if console_logger:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logger.level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Prevent log messages from being propagated to the root logger
        # logger.propagate = False

    return logger


def get_logger(logger_name: str = LOGGER) -> logging.Logger:
    """
    Returns the configured logger.

    Args:
        logger_name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: The configured logger.
    """
    return logging.getLogger(logger_name)
