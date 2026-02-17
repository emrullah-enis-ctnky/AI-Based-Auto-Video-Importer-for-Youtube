import logging
import os
import sys
from datetime import datetime

class AppLogger:
    """
    Custom logger that provides concise terminal output and detailed file output.
    """
    def __init__(self, name="AI_YouTube_Commiter"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers if logger is already initialized
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, "app.log")

        # 1. File Handler (Detailed)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # 2. Console Handler (Concise)
        console_formatter = logging.Formatter('%(message)s')
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(f"⚠️  {msg}")

    def error(self, msg, exc_info=True):
        self.logger.error(f"❌ {msg}", exc_info=exc_info)

    def success(self, msg):
        self.logger.info(f"✅ {msg}")

# Global instance
logger = AppLogger()
