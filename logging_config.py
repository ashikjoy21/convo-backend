import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'logs/app.log',
                maxBytes=10000000,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )

    # Set specific logger levels
    logging.getLogger('quart.app').setLevel(logging.WARNING)
    logging.getLogger('quart.serving').setLevel(logging.WARNING) 