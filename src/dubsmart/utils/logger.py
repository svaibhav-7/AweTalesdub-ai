import logging
import os
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Initialize and return a logger with a standard format.
    
    Args:
        name: The name of the logger (usually __name__)
        
    Returns:
        A configured logging.Logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # File handler (logs/dubsmart.log)
        try:
            os.makedirs('logs', exist_ok=True)
            file_handler = logging.FileHandler('logs/dubsmart.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            # Fallback if log directory is not writable
            pass
            
    return logger
