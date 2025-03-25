"""
logger.py

This module sets up a logger that logs messages to both the console and a file.
It ensures logs are stored in a dedicated directory with a timestamped filename.

Author: [YAquil Iqbal]
Email : [aquiliqbal14@gmail.com]
"""

from datetime import datetime
import logging
import os


def setup_logger(log_level: str) -> logging.Logger:
    """
    Setup the logger with the specified log level.

    Args:
        log_level (str): The log level to set for the logger.

    Returns:
        logging.Logger: The configured logger object.
    """
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    try:
        log_dir = "logs"
        if not os.path.exists(log_dir):
            # Create the logs directory if it does not exist
            os.makedirs(log_dir)

        log_filename = f"{log_dir}/corona_da_{timestamp}.log"

        logger = logging.getLogger()
        # Set the log level for the logger
        logger.setLevel(log_level)

        # Remove all handlers associated with the root logger object
        # This is done to prevent duplicate log messages
        for handler in list(logger.handlers):
            logger.removeHandler(handler)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_filename)

        # Set the log level for the console and file handlers
        console_handler.setLevel(log_level)
        file_handler.setLevel(log_level)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        # Set the formatter for the console and file handlers
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add the console and file handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
    except Exception as e:
        logger.error(e)
