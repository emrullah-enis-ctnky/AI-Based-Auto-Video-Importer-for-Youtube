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
    
    args = parser.parse_args()
    
    video_path = args.video
    thumbnail_path = args.thumbnail
    
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
        logger.info("Thumbnail (Küçük Resim) seçilmesi bekleniyor...")
        thumbnail_path = get_file_dialog(
            "Thumbnail (Küçük Resim) Seçin", 
            [("Resim Dosyaları", "*.jpg *.jpeg *.png"), ("Tüm Dosyalar", "*.*")]
        )
        if not thumbnail_path:
            logger.error("Thumbnail seçilmedi. İşlem iptal ediliyor.")
            sys.exit(1)
        logger.info(f"Seçilen Thumbnail: {os.path.basename(thumbnail_path)}")

    # Validate existence
    if not os.path.exists(video_path):
        logger.error(f"Video dosyası bulunamadı: {video_path}")
        sys.exit(1)
    
    if not os.path.exists(thumbnail_path):
        logger.error(f"Thumbnail dosyası bulunamadı: {thumbnail_path}")
        sys.exit(1)
        
    return video_path, thumbnail_path

if __name__ == "__main__":
    v, t = get_inputs()
    print(f"Video: {v}\nThumbnail: {t}")
