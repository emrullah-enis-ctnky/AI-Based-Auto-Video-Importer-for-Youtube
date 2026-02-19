import threading
import time
import os
from utils.logger import logger
from gemini.analyzer import analyze_content
from youtube.auth import get_youtube_service
from youtube.uploader import upload_video
from youtube.thumbnail import set_thumbnail
from utils.app_init import initialize_app

from .styles import Localizer

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
            self.page.write_log(Localizer.translate("processing") + "...")
            
            # --- Initialize and Setup Logger ---
            if not initialize_app():
                self.page.write_log("ERROR: initialize_app() FAILED")
                return

            if debug_mode:
                import logging
                # Set both our custom logger and root logger to DEBUG
                logger.setLevel("DEBUG") 
                self.page.write_log("DEBUG MODE: ON")

            # --- STAGE 1: AI Analysis ---
            self.page.write_log(f"1/2: {Localizer.translate('ai_analysis')}...")
            
            metadata = analyze_content(
                video_path, thumb_path, user_notes, use_compression, 
                progress_callback=self.page.update_progress
            )
            
            if not metadata:
                self.page.write_log("HATA: AI Analysis FAILED")
                self.page.ai_progress.configure(progress_color="red")
                return

            self.page.update_progress("ai", 1.0)
            self.page.write_log(f"AI: {metadata.title}")

            # --- STAGE 2: YouTube Upload ---
            self.page.write_log(f"2/2: {Localizer.translate('yt_upload')}...")
            
            youtube = get_youtube_service()
            if not youtube:
                self.page.write_log("HATA: YouTube Auth FAILED")
                return

            video_id = upload_video(
                youtube, video_path, metadata, 
                progress_callback=self.page.update_progress
            )
            
            if not video_id:
                self.page.write_log("HATA: Upload FAILED")
                self.page.upload_progress.configure(progress_color="red")
                return

            # FORCE 100% AFTER UPLOAD
            self.page.update_progress("upload", 1.0)
            
            if thumb_path:
                self.page.write_log(f"{Localizer.translate('thumb_upload')}...")
                try:
                    set_thumbnail(youtube, video_id, thumb_path)
                except Exception as te:
                    self.page.write_log(f"Info: Thumbnail error (skipped): {str(te)}")
            
            self.page.write_log(Localizer.translate("all_done"))
            self.page.write_log(f"{Localizer.translate('video_link')} https://youtu.be/{video_id}")
            
            # Show finish button and hide control buttons
            def finalize_ui():
                self.page.back_btn.grid_remove()
                self.page.log_btn.grid_remove()
                self.page.finish_btn.grid(row=0, column=0, columnspan=2)
            
            self.app.after(500, finalize_ui)

        except Exception as e:
            self.page.write_log(f"BEKLENMEDİK HATA: {str(e)}")
            logger.error(f"Bridge error: {str(e)}")
