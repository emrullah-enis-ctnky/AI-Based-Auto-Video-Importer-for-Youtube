import os
import sys
from dotenv import load_dotenv
from .logger import logger

class Config:
    """
    Handles environment variables and application configuration.
    """
    def __init__(self):
        load_dotenv()
        
        # Required Keys
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        
        # Paths
        self.ROOT_DIR = os.getcwd()
        if getattr(sys, 'frozen', False):
            # If frozen, the executable might be in a different place, 
            # but we usually want persistent files in the CWD or executable's directory.
            # Using CWD for now as it's common for CLI/GUI tools to look in the folder they are run from.
            self.BASE_DIR = os.getcwd()
        else:
            self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        self.CLIENT_SECRET_FILE = os.path.join(self.BASE_DIR, os.getenv("CLIENT_SECRET_FILE", "client_secret.json"))
        self.TOKEN_FILE = os.path.join(self.BASE_DIR, "token.pickle")
        
        # Optional / Derived
        self.LOG_DIR = os.path.join(self.BASE_DIR, "logs")
        self.LOG_FILE = os.path.join(self.LOG_DIR, "app.log")

    def get(self, key, default=None):
        """
        Retrieves a configuration value by key.
        """
        return getattr(self, key, default)

    def validate(self):
        """
        Validates that all required environment variables are set.
        Returns:
            bool: True if valid, raises ValueError otherwise.
        """
        missing = []
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        
        if missing:
            err_msg = f"Missing environment variables: {', '.join(missing)}. Please check your .env file."
            logger.error(err_msg)
            raise ValueError(err_msg)
            
        logger.debug("Configuration validated successfully.")
        return True

# Global instance
config = Config()
