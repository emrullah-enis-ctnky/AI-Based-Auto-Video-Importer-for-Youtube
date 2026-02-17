import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from utils.app_init import initialize_app
from utils.dep_manager import check_and_install_dependencies
from utils.input_handler import get_inputs
from utils.logger import logger

def main():
    """
    Main orchestration function.
    """
    # 0. Stylish Banner
    logger.banner("🚀 AI-Powered YouTube Automation Tool")

    # 1. Initialize Folders and Config
    logger.step(1, "Sistem Başlatılıyor")
    if not initialize_app():
        sys.exit(1)
        
    # 2. Check/Install Dependencies
    logger.step(2, "Bağımlılık Kontrolü")
    check_and_install_dependencies()
    
    # 3. Get Inputs (CLI or GUI)
    logger.step(3, "Giriş Bilgileri")
    video_path, thumbnail_path = get_inputs()
    
    logger.success("Giriş verileri başarıyla alındı.")
    logger.info(f"Video: {video_path}")
    logger.info(f"Thumbnail: {thumbnail_path}")
    
    # Future Phases will continue here:
    # Phase 3: AI Analysis
    # Phase 4: YouTube Upload
    
    logger.info("\nŞu anlık bu kadar! Phase 2 tamamlandı. AI Analiz aşaması için beklemede kalın.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmedik bir hata oluştu: {str(e)}")
        sys.exit(1)
