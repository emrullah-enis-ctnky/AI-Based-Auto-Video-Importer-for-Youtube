import customtkinter as ctk
from gui.styles import PADDING, CORNER_RADIUS, FONTS, ThemeManager, Localizer
import os

class LogWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sistem Logları")
        self.geometry("800x600")
        self.attributes("-topmost", True)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.log_text = ctk.CTkTextbox(
            self, corner_radius=CORNER_RADIUS, 
            font=FONTS["mono"], fg_color="black", text_color="#00FF41"
        )
        self.log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_text.configure(state="disabled")

    def write_log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

class ProcessPage(ctk.CTkFrame):
    def __init__(self, master, video_path, thumb_path, user_notes, use_compression, debug_mode, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Outer centering

        # Internal container for all elements (centered)
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0)
        self.container.grid_columnconfigure(0, weight=1)

        # 1. Header (Centered)
        self.header_label = ctk.CTkLabel(self.container, text=Localizer.translate("processing"), font=FONTS["title"])
        self.header_label.grid(row=0, column=0, padx=PADDING, pady=(0, 50))

        # 2. Centered Progress Section
        self.progress_frame = ctk.CTkFrame(self.container, fg_color=("gray90", "gray15"), corner_radius=CORNER_RADIUS)
        self.progress_frame.grid(row=1, column=0, padx=PADDING, pady=10, ipadx=40, ipady=40)
        self.progress_frame.configure(width=850, height=350) 
        self.progress_frame.grid_propagate(False) 
        self.progress_frame.grid_columnconfigure(0, weight=1)

        # AI Analysis Progress
        self.ai_label_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.ai_label_frame.grid(row=0, column=0, sticky="ew", padx=PADDING, pady=(20, 5))
        self.ai_label_frame.grid_columnconfigure(1, weight=1)

        self.ai_label = ctk.CTkLabel(self.ai_label_frame, text=Localizer.translate("ai_analysis"), font=FONTS["header"])
        self.ai_label.grid(row=0, column=0, sticky="w")
        
        self.ai_pc_label = ctk.CTkLabel(self.ai_label_frame, text="%0", font=FONTS["header"], text_color=("#002171", "#00E5FF"))
        self.ai_pc_label.grid(row=0, column=1, sticky="e")
        
        self.ai_progress = ctk.CTkProgressBar(self.progress_frame, height=25, progress_color=("#002171", "#00E5FF"))
        self.ai_progress.grid(row=1, column=0, padx=PADDING, pady=(0, 40), sticky="ew")
        self.ai_progress.set(0)

        # YouTube Upload Progress
        self.upload_label_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.upload_label_frame.grid(row=2, column=0, sticky="ew", padx=PADDING, pady=(0, 5))
        self.upload_label_frame.grid_columnconfigure(1, weight=1)

        self.upload_label = ctk.CTkLabel(self.upload_label_frame, text=Localizer.translate("yt_upload"), font=FONTS["header"])
        self.upload_label.grid(row=0, column=0, sticky="w")
        
        self.upload_pc_label = ctk.CTkLabel(self.upload_label_frame, text="%0", font=FONTS["header"], text_color=("#002171", "#00E5FF"))
        self.upload_pc_label.grid(row=0, column=1, sticky="e")
        
        self.upload_progress = ctk.CTkProgressBar(self.progress_frame, height=25, progress_color=("#002171", "#00E5FF"))
        self.upload_progress.grid(row=3, column=0, padx=PADDING, pady=0, sticky="ew")
        self.upload_progress.set(0)

        # 3. Action Buttons
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=PADDING, pady=60)

        self.back_btn = ctk.CTkButton(
            self.button_frame, text=Localizer.translate("cancel_btn"), height=50, width=200,
            fg_color="gray40", hover_color="gray50", command=self.on_cancel
        )
        self.back_btn.grid(row=0, column=0, padx=10)

        self.log_btn = ctk.CTkButton(
            self.button_frame, text=Localizer.translate("logs_btn"), height=50, width=200,
            fg_color="transparent", border_width=2, text_color=ThemeManager.get_tuple("accent"),
            command=self.toggle_logs
        )
        self.log_btn.grid(row=0, column=1, padx=10)

        self.finish_btn = ctk.CTkButton(
            self.button_frame, text=Localizer.translate("finish_btn"), height=60, width=400,
            fg_color=("#002171", "#05E5FF"), text_color=("white", "black"), font=("Arial", 18, "bold"),
            command=self.on_finish
        )

        # State for logs
        self.log_window = None
        self.logs_history = []

        # Start simulation/task
        self.start_automation(video_path, thumb_path, user_notes, use_compression, debug_mode)

    def refresh_localization(self):
        self.header_label.configure(text=Localizer.translate("processing"))
        self.ai_label.configure(text=Localizer.translate("ai_analysis"))
        self.upload_label.configure(text=Localizer.translate("yt_upload"))
        self.log_btn.configure(text=Localizer.translate("logs_btn"))
        self.back_btn.configure(text=Localizer.translate("cancel_btn"))
        self.finish_btn.configure(text=Localizer.translate("finish_btn"))

    def write_log(self, message):
        msg = f"> {message}"
        self.logs_history.append(msg)
        if self.log_window and self.log_window.winfo_exists():
            self.log_window.write_log(message)

    def toggle_logs(self):
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = LogWindow(self)
            for old_msg in self.logs_history:
                self.log_window.write_log(old_msg.replace("> ", ""))
        else:
            self.log_window.focus()

    def update_progress(self, stage, value):
        pc = int(value * 100)
        if stage == "ai":
            self.ai_progress.set(value)
            self.ai_pc_label.configure(text=f"%{pc}")
        elif stage == "upload":
            self.upload_progress.set(value)
            self.upload_pc_label.configure(text=f"%{pc}")

    def start_automation(self, video_path, thumb_path, user_notes, use_compression, debug_mode):
        from gui.bridge import AutomationBridge
        self.bridge = AutomationBridge(self.winfo_toplevel(), self)
        self.bridge.start(video_path, thumb_path, user_notes, use_compression, debug_mode)

    def on_cancel(self):
        from tkinter import messagebox
        if messagebox.askyesno("Onay", "İşlemi iptal etmek istediğinize emin misiniz?"):
            self.winfo_toplevel().show_home() 

    def on_finish(self):
        if self.log_window and self.log_window.winfo_exists():
            self.log_window.destroy()
        self.winfo_toplevel().show_home()
