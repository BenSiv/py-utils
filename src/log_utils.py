import os
import logging
import sys

def setup_logging(log_dir: str, log_name: str = "app.log") -> None:
    """Sets up logging to file and console."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, log_name)
    
    # Configure logging
    # Note: This might overwrite existing config if called multiple times
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info(f"Logging setup complete. Log file: {log_file}")
