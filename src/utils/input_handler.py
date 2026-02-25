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
    parser.add_argument("--video", type=str, required=True, help="Path to the video file")
    parser.add_argument("--thumbnail", type=str, help="Path to the thumbnail image (optional)")
    parser.add_argument("--playlist", type=str, help="YouTube playlist title to add the video to (optional)")
    parser.add_argument("--notes", type=str, help="Extra notes for AI analysis")
    parser.add_argument("--debug", action="store_true", help="Enable detailed debug logging")
    parser.add_argument("--no-ai", action="store_true", help="Disable AI analysis and use manual metadata")
    parser.add_argument("--title", type=str, help="Manual title for the video (used with --no-ai)")
    parser.add_argument("--description", type=str, help="Manual description for the video (used with --no-ai)")
    parser.add_argument("--tags", type=str, help="Manual tags for the video, comma-separated (used with --no-ai)")
    
    args = parser.parse_args()
    
    video_path = args.video
    thumbnail_path = args.thumbnail
    user_notes = args.notes
    playlist_title = args.playlist
    no_ai = args.no_ai
    manual_title = args.title
    manual_description = args.description
    manual_tags = args.tags
    
    # GUI fallbacks removed to ensure pure CLI experience.
    # missing --video will be caught by argparse (required=True).
    # missing --thumbnail will simply be None (optional).

    # Interactive input for notes if not provided and AI is enabled
    if not no_ai and not user_notes:
        from rich.prompt import Prompt
        user_notes = Prompt.ask("\n[bold cyan]AI için ek notlarınız veya talimatlarınız var mı?[/bold cyan] (Boş bırakılabilir)", default="")
        if user_notes:
            logger.info(f"Notunuz kaydedildi: {user_notes}")
        else:
            logger.info("Ek not belirtilmedi.")

    # Playlist input (Interactive prompt removed to keep it optional and fast)
    if not playlist_title:
        # We don't force a prompt here to keep it strictly optional as per "ek bir parametre" request.
        pass

    # Compression Check & Prompt (Only if AI is enabled)
    from .media_processor import is_ffmpeg_installed
    from rich.prompt import Confirm
    
    use_compression = False
    if not no_ai:
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
        
    return video_path, thumbnail_path, user_notes, args.debug, use_compression, playlist_title, no_ai, manual_title, manual_description, manual_tags

if __name__ == "__main__":
    v, t = get_inputs()
    print(f"Video: {v}\nThumbnail: {t}")
