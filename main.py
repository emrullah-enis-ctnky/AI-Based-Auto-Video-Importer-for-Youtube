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

    # 4. AI Analysis
    logger.step(4, "AI Video Analizi")
    from gemini.analyzer import analyze_video
    from rich.panel import Panel
    from rich.table import Table
    
    metadata = analyze_video(video_path)
    
    if metadata:
        logger.success("AI Analizi başarıyla tamamlandı!")
        
        # Display Results
        table = Table(title="Generate Edilen Metadata", show_header=True, header_style="bold magenta")
        table.add_column("Alan", style="cyan", width=12)
        table.add_column("İçerik", style="white")
        
        table.add_row("Başlık", metadata.title)
        table.add_row("Açıklama", metadata.description[:200] + "..." if len(metadata.description) > 200 else metadata.description)
        table.add_row("Etiketler", ", ".join(metadata.tags))
        
        from utils.logger import console
        console.print(table)
    else:
        logger.error("AI Analizi başarısız oldu. Lütfen logları kontrol edin.")
        sys.exit(1)
    
    # Future Phases will continue here:
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
