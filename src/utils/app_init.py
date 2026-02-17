import os
from .logger import logger
from .config import config

def ensure_directories():
    """
    Ensures all required project directories exist.
    """
    dirs = [
        "logs",
        "src/api",
        "src/gemini",
        "src/youtube",
        "src/video_analiz",
        "src/video_yukleme",
        "src/utils"
    ]
    
    for d in dirs:
        path = os.path.join(os.getcwd(), d)
        if not os.path.exists(path):
            os.makedirs(path)
            logger.debug(f"Created directory: {d}")

def initialize_app():
    """
    Main initialization sequence for the application.
    """
    try:
        logger.info("Sistem başlatılıyor...")
        ensure_directories()
        config.validate()
        logger.success("Sistem hazır.")
        return True
    except Exception as e:
        logger.error(f"Başlatma hatası: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_app()
