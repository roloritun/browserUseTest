import logging
import os

def configure_logging(log_file="app.log", log_level=logging.INFO):
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)
    log_file_path = os.path.join("logs", log_file)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
