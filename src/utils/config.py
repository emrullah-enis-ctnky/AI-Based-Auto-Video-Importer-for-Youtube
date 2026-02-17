import os
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
        self.CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE", "client_secret.json")
        
        # Optional / Derived
        self.LOG_DIR = os.path.join(os.getcwd(), "logs")
        self.LOG_FILE = os.path.join(self.LOG_DIR, "app.log")

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
