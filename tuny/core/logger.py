"""Logging configuration"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

def setup_logging(app):
    """
    Configure logging for the application
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_dir = 'logs'
    
    # Create logs directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler with JSON format
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'tuny.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(log_level)
    json_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(json_formatter)
    
    # Add handlers to app logger
    app.logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
