import customtkinter as ctk
from ..styles import PADDING, CORNER_RADIUS, FONTS, ThemeManager
import os

class ProcessPage(ctk.CTkFrame):
    def __init__(self, master, video_path, thumb_path, user_notes, use_compression, debug_mode, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # 1. Header
        self.header_label = ctk.CTkLabel(self, text="Otomasyon Devam Ediyor", font=FONTS["title"])
        self.header_label.grid(row=0, column=0, padx=PADDING, pady=(10, 30), sticky="w")

        # 2. Progress Section
        self.progress_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray15"), corner_radius=CORNER_RADIUS)
        self.progress_frame.grid(row=1, column=0, padx=PADDING, pady=10, sticky="ew", ipadx=20, ipady=20)
        self.progress_frame.grid_columnconfigure(0, weight=1)

        # AI Analysis Progress
        self.ai_label = ctk.CTkLabel(self.progress_frame, text="AI İçerik Analizi", font=FONTS["header"])
        self.ai_label.grid(row=0, column=0, padx=PADDING, pady=(10, 5), sticky="w")
        
        self.ai_progress = ctk.CTkProgressBar(self.progress_frame, height=15)
        self.ai_progress.grid(row=1, column=0, padx=PADDING, pady=(0, 20), sticky="ew")
        self.ai_progress.set(0)

        # YouTube Upload Progress
        self.upload_label = ctk.CTkLabel(self.progress_frame, text="YouTube Yükleme", font=FONTS["header"])
        self.upload_label.grid(row=2, column=0, padx=PADDING, pady=(10, 5), sticky="w")
        
        self.upload_progress = ctk.CTkProgressBar(self.progress_frame, height=15)
        self.upload_progress.grid(row=3, column=0, padx=PADDING, pady=(0, 20), sticky="ew")
        self.upload_progress.set(0)

        # 3. Live Logs Section
        self.log_label = ctk.CTkLabel(self, text="Sistem Logları", font=FONTS["header"])
        self.log_label.grid(row=2, column=0, padx=PADDING, pady=(20, 5), sticky="w")
        
        self.log_text = ctk.CTkTextbox(
            self, height=300, corner_radius=CORNER_RADIUS, 
            font=FONTS["mono"], fg_color="black", text_color="#00FF41" # Matrix/Terminal style
        )
        self.log_text.grid(row=3, column=0, padx=PADDING, pady=5, sticky="nsew")
        self.log_text.configure(state="disabled")

        # 4. Action Buttons (Hidden until finish)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, padx=PADDING, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.back_btn = ctk.CTkButton(
            self.button_frame, text="VAZGEÇ", height=50, 
            fg_color="gray40", hover_color="gray50", command=self.on_cancel
        )
        self.back_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.finish_btn = ctk.CTkButton(
            self.button_frame, text="BİTİR VE ANA SAYFAYA DÖN", height=50,
            fg_color="#00E5FF", text_color="black", font=("Arial", 18, "bold"),
            command=self.on_finish
        )
        self.finish_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.finish_btn.grid_remove() # Hide initially

        # Start simulation/task
        self.start_automation(video_path, thumb_path, user_notes, use_compression, debug_mode)

    def write_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def update_progress(self, stage, value):
        if stage == "ai":
            self.ai_progress.set(value)
        elif stage == "upload":
            self.upload_progress.set(value)

    def start_automation(self, video_path, thumb_path, user_notes, use_compression, debug_mode):
        self.write_log("Otomasyon köprüsü başlatılıyor...")
        from ..bridge import AutomationBridge
        
        # Accessing YouTubeAutomationApp (master is main_content_frame, master.master is app)
        self.bridge = AutomationBridge(self.master.master, self)
        self.bridge.start(video_path, thumb_path, user_notes, use_compression, debug_mode)

    def on_cancel(self):
        # Handle cancellation
        from tkinter import messagebox
        if messagebox.askyesno("Onay", "İşlemi iptal etmek istediğinize emin misiniz?"):
            self.master.master.show_home() 

    def on_finish(self):
        self.master.master.show_home()
