import logging
import logging.handlers
import os
from datetime import datetime

LOG_DIR = "jules" # As per user's earlier request for a 'jules' folder

def setup_logging(log_level_str='INFO', log_dir=LOG_DIR):
    '''
    Sets up application-wide logging.

    Logs will be written to a timestamped file in the specified directory.
    Example: jules/app_20231027.log
    '''
    numeric_level = getattr(logging, log_level_str.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level_str}')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d')}.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')

    # Set up root logger
    # Using root logger for simplicity here, can be changed to a specific app logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicate logs if setup_logging is called multiple times
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # Console Handler (optional, good for immediate feedback during dev)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level) # Or a different level for console
    root_logger.addHandler(console_handler)

    # File Handler (writes to jules/app_YYYYMMDD.log)
    # Using TimedRotatingFileHandler for daily rotation
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(numeric_level)
    root_logger.addHandler(file_handler)

    logging.info("Logging setup complete. Log level: %s. Log file: %s", log_level_str, log_filename)
    return root_logger # Or just logger for a specific app logger
