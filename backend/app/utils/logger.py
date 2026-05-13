"""
Jinja SSS Platform - Logging Configuration
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(env='development'):
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if env == 'development' else logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if env == 'development' else logging.INFO)
    console.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s' if env == 'development'
        else '{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}'
    ))
    logger.addHandler(console)

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10*1024*1024, backupCount=30)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(file_handler)

    return logger


def get_logger(name):
    return logging.getLogger(name)
