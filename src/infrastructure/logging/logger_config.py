"""Logging configuration for Core Web Vitals application."""
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = 'INFO',
    log_dir: Optional[str] = None,
    log_to_file: bool = True,
    log_to_console: bool = True,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (defaults to ./logs)
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console
    """
    # Get log level from environment or parameter
    level_name = os.getenv('LOG_LEVEL', log_level).upper()
    level = getattr(logging, level_name, logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)

    # File handler
    if log_to_file:
        # Ensure log directory exists
        if log_dir is None:
            log_dir = os.path.join(os.getcwd(), 'logs')
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'cwv_job_{timestamp}.log')

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)

        # Log the file location
        root_logger.info(f"Logging to file: {log_file}")

    # Reduce noise from third-party libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('mysql.connector').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
