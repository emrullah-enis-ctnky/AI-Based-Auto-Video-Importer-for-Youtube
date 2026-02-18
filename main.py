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
    
    # 5. YouTube Automation
    logger.step(5, "YouTube Yükleme")
    from youtube.auth import get_youtube_service
    from youtube.uploader import upload_video
    from youtube.thumbnail import set_thumbnail
    
    youtube = get_youtube_service()
    if not youtube:
        logger.error("YouTube bağlantısı kurulamadı. Lütfen client_secret.json dosyasını ve internet bağlantınızı kontrol edin.")
        sys.exit(1)
        
    video_id = upload_video(youtube, video_path, metadata)
    
    if video_id:
        if thumbnail_path:
            set_thumbnail(youtube, video_id, thumbnail_path)
        
        logger.banner("🎉 İŞLEM BAŞARIYLA TAMAMLANDI")
        logger.success(f"Videonuz YouTube'a yüklendi (Gizli): https://youtu.be/{video_id}")
    else:
        logger.error("Video yüklenemedi. Detaylar için logs/app.log dosyasına bakın.")
        sys.exit(1)

    logger.info("\nProje Phase 4 tamamlandı! Artık tam otomatik video analizi ve yükleme yapabiliyoruz.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmedik bir hata oluştu: {str(e)}")
        sys.exit(1)
