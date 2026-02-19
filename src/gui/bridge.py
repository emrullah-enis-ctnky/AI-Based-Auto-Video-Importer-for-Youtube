import threading
import time
import os
from utils.logger import logger
from gemini.analyzer import analyze_content
from youtube.auth import get_youtube_service
from youtube.uploader import upload_video
from youtube.thumbnail import set_thumbnail
from utils.app_init import initialize_app

class AutomationBridge:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.thread = None
        self.stop_requested = False

    def start(self, video_path, thumb_path, user_notes, use_compression, debug_mode):
        self.thread = threading.Thread(
            target=self._run_automation,
            args=(video_path, thumb_path, user_notes, use_compression, debug_mode),
            daemon=True
        )
        self.thread.start()

    def _run_automation(self, video_path, thumb_path, user_notes, use_compression, debug_mode):
        try:
            self.page.write_log("Sistem ön hazırlıkları yapılıyor...")
            if not initialize_app():
                self.page.write_log("HATA: Sistem başlatılamadı.")
                return

            if debug_mode:
                import logging
                logger.logger.setLevel(logging.DEBUG)

            # --- STAGE 1: AI Analysis ---
            self.page.write_log("Aşama 1: AI Analizi başlatılıyor...")
            
            # Use real callbacks for progress
            metadata = analyze_content(
                video_path, thumb_path, user_notes, use_compression, 
                progress_callback=self.page.update_progress
            )
            
            if not metadata:
                self.page.write_log("HATA: AI Analizi başarısız.")
                self.page.ai_progress.configure(progress_color="red")
                return

            self.page.write_log(f"AI Analizi Tamamlandı: {metadata.title}")

            # --- STAGE 2: YouTube Upload ---
            self.page.write_log("Aşama 2: YouTube Yükleme başlatılıyor...")
            
            youtube = get_youtube_service()
            if not youtube:
                self.page.write_log("HATA: YouTube bağlantısı kurulamadı.")
                return

            # Pass same callback to uploader
            video_id = upload_video(
                youtube, video_path, metadata, 
                progress_callback=self.page.update_progress
            )
            
            if not video_id:
                self.page.write_log("HATA: Video yüklenemedi.")
                self.page.upload_progress.configure(progress_color="red")
                return

            self.page.update_progress("upload", 0.8)
            
            if thumb_path:
                self.page.write_log("Kapak fotoğrafı ayarlanıyor...")
                set_thumbnail(youtube, video_id, thumb_path)
            
            self.page.update_progress("upload", 1.0)
            self.page.write_log("✅ Tüm işlemler başarıyla tamamlandı!")
            self.page.write_log(f"Video Linki: https://youtu.be/{video_id}")
            
            # Show finish button
            self.app.after(500, self.page.finish_btn.grid)

        except Exception as e:
            self.page.write_log(f"BEKLENMEDİK HATA: {str(e)}")
            logger.error(f"Bridge error: {str(e)}")
