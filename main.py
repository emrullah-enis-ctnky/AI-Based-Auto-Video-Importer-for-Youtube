import sys
import os

# Setup pathing: Add 'src' to path in development mode.
# In PyInstaller frozen mode, modules are bundled and reachable via standard imports.
if not getattr(sys, 'frozen', False):
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(bundle_dir, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

from utils.app_init import initialize_app
from utils.dep_manager import check_and_install_dependencies
from utils.input_handler import get_inputs
from utils.logger import logger

def main():
    """
    Main orchestration function.
    """
    # 0. Check for CLI mode vs GUI mode
    import sys
    
    # If any arguments besides the script name are passed, run in CLI mode.
    # Otherwise, fire up the GUI.
    if len(sys.argv) > 1:
        logger.banner("🚀 AI-Powered YouTube Automation Tool (CLI Mode)")
        
        # 1. Initialize Folders and Config
        logger.step(1, "Sistem Başlatılıyor")
        if not initialize_app():
            sys.exit(1)
            
        # 2. Check/Install Dependencies
        logger.step(2, "Bağımlılık Kontrolü")
        check_and_install_dependencies()
        
        # 3. Get Inputs (CLI or GUI dialogs)
        logger.step(3, "Giriş Bilgileri")
        video_path, thumbnail_path, user_notes, debug_mode, use_compression, playlist_title = get_inputs()
        
        if debug_mode:
            import logging
            logger.logger.setLevel(logging.DEBUG)
            logger.info("Debug modu aktif edildi. Detaylı loglar gösteriliyor.")
        
        logger.success("Giriş verileri başarıyla alındı.")
    else:
        # Launch Graphical User Interface
        try:
            from gui.app import YouTubeAutomationApp
            app = YouTubeAutomationApp()
            app.mainloop()
            return # Exit cleanly after GUI closes
        except Exception as e:
            # Use standard print as well to ensure visibility if logger fails
            print(f"\nCRITICAL GUI ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            logger.error(f"Arayüz (GUI) başlatılamadı: {str(e)}")
            sys.exit(1)

    # 4. AI Analysis
    logger.step(4, "AI Multimodal Analiz (Video + Görsel + Notlar)")
    from gemini.analyzer import analyze_content
    from rich.panel import Panel
    from rich.table import Table
    
    metadata = analyze_content(video_path, thumbnail_path, user_notes, use_compression)
    
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
    from youtube.playlist import get_or_create_playlist, add_video_to_playlist
    
    youtube = get_youtube_service()
    if not youtube:
        logger.error("YouTube bağlantısı kurulamadı. Lütfen client_secret.json dosyasını ve internet bağlantınızı kontrol edin.")
        sys.exit(1)
        
    video_id = upload_video(youtube, video_path, metadata)
    
    if video_id:
        if thumbnail_path:
            set_thumbnail(youtube, video_id, thumbnail_path)
            
        if playlist_title:
            logger.info(f"Oynatma listesi işlemleri başlatılıyor: {playlist_title}")
            playlist_id = get_or_create_playlist(youtube, playlist_title)
            if playlist_id:
                add_video_to_playlist(youtube, video_id, playlist_id)
        
        # Her Şey Hazır - Final Effect
        logger.banner("✨ İŞLEM BAŞARIYLA TAMAMLANDI")
        
        summary_panel = Panel(
            f"[bold cyan]DURUM         :[/bold cyan] [bold green]ÇEVRİMİÇİ[/bold green]\n"
            f"[bold cyan]VİDEO ID      :[/bold cyan] [white]{video_id}[/white]\n"
            f"[bold cyan]YOUTUBE LİNKİ :[/bold cyan] [underline blue]https://youtu.be/{video_id}[/underline blue]\n"
            f"[bold cyan]GİZLİLİK      :[/bold cyan] [bold yellow]ÖZEL (PRIVATE)[/bold yellow]\n"
            f"[bold cyan]AI ANALİZİ    :[/bold cyan] [italic magenta]MULTIMODAL TAMAMLANDI[/italic magenta]\n\n"
            "[bold green]>>> HER ŞEY HAZIR. GÖREV TAMAMLANDI. <<<[/bold green]",
            title="[bold white]SİSTEM ÖZETİ[/bold white]",
            border_style="bold cyan",
            padding=(1, 2)
        )
        console.print(summary_panel)
    else:
        logger.error("HATA: Video yüklenemedi.")
        sys.exit(1)

    logger.info("\n[bold cyan]Proje v1.0 - Tüm sistem optimizasyonları devrede.[/bold cyan]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmedik bir hata oluştu: {str(e)}")
        sys.exit(1)
