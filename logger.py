import logging
import sys

def setup_logger():
    logger = logging.getLogger('TokyoTrainAlert')
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler('alerts.log')
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger