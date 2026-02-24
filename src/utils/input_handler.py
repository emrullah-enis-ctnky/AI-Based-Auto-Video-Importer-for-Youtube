import argparse
import os
import sys
import tkinter as tk
from tkinter import filedialog
from .logger import logger

def get_file_dialog(title, filetypes):
    """
    Opens a file dialog to select a file.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    root.attributes('-topmost', True)  # Bring dialog to front
    
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path

def get_inputs():
    """
    Gets video and thumbnail paths from CLI arguments or file dialogs.
    """
    parser = argparse.ArgumentParser(description="AI-Powered YouTube Automation Tool")
    parser.add_argument("--video", type=str, help="Path to the video file")
    parser.add_argument("--thumbnail", type=str, help="Path to the thumbnail image")
    parser.add_argument("--notes", type=str, help="Extra notes for AI analysis")
    parser.add_argument("--debug", action="store_true", help="Enable detailed debug logging")
    
    args = parser.parse_args()
    
    video_path = args.video
    thumbnail_path = args.thumbnail
    user_notes = args.notes
    
    # Fallback to File Dialog for Video
    if not video_path:
        logger.info("Video dosyası seçilmesi bekleniyor...")
        video_path = get_file_dialog(
            "Video Dosyasını Seçin", 
            [("Video Dosyaları", "*.mp4 *.mov *.avi *.mkv"), ("Tüm Dosyalar", "*.*")]
        )
        if not video_path:
            logger.error("Video seçilmedi. İşlem iptal ediliyor.")
            sys.exit(1)
        logger.info(f"Seçilen Video: {os.path.basename(video_path)}")

    # Fallback to File Dialog for Thumbnail
    if not thumbnail_path:
        logger.info("Thumbnail (Küçük Resim) seçimi isteğe bağlıdır. Atlamak için iptal edebilirsiniz.")
        thumbnail_path = get_file_dialog(
            "Thumbnail (Küçük Resim) Seçin (Opsiyonel)", 
            [("Resim Dosyaları", "*.jpg *.jpeg *.png"), ("Tüm Dosyalar", "*.*")]
        )
        if thumbnail_path:
            logger.info(f"Seçilen Thumbnail: {os.path.basename(thumbnail_path)}")
        else:
            logger.info("Thumbnail seçilmedi, işleme thumbnailsiz devam edilecek.")
            thumbnail_path = None

    # Interactive input for notes if not provided
    if not user_notes:
        from rich.prompt import Prompt
        user_notes = Prompt.ask("\n[bold cyan]AI için ek notlarınız veya talimatlarınız var mı?[/bold cyan] (Boş bırakılabilir)", default="")
        if user_notes:
            logger.info(f"Notunuz kaydedildi: {user_notes}")
        else:
            logger.info("Ek not belirtilmedi.")

    # Compression Check & Prompt
    from .media_processor import is_ffmpeg_installed
    from rich.prompt import Confirm
    
    use_compression = False
    if is_ffmpeg_installed():
        use_compression = Confirm.ask("\n[bold yellow]Hızlı AI Analizi (Sıkıştırma) aktif edilsin mi?[/bold yellow]", default=True)
        if use_compression:
            logger.info("Medya sıkıştırma aktif. Analiz aşaması hızlanacak.")
    else:
        logger.warning("\n[bold red]Sistemde FFmpeg bulunamadı.[/bold red]")
        logger.info("Daha hızlı analiz ve düşük kota kullanımı için FFmpeg kurmanız önerilir.")
        logger.info("Şu anlık orijinal büyük dosyalar gönderilecek.")

    # Validate existence
    if not os.path.exists(video_path):
        logger.error(f"Video dosyası bulunamadı: {video_path}")
        sys.exit(1)
    
    if thumbnail_path and not os.path.exists(thumbnail_path):
        logger.error(f"Thumbnail dosyası bulunamadı: {thumbnail_path}")
        sys.exit(1)
        
    return video_path, thumbnail_path, user_notes, args.debug, use_compression

if __name__ == "__main__":
    v, t = get_inputs()
    print(f"Video: {v}\nThumbnail: {t}")
