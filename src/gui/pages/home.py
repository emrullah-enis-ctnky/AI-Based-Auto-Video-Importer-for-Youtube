import customtkinter as ctk
from ..styles import PADDING, CORNER_RADIUS, FONTS, ThemeManager
from tkinter import filedialog
from PIL import Image
import os
import subprocess
import time

class MediaCard(ctk.CTkButton):
    def __init__(self, master, title, placeholder, icon_path, command, **kwargs):
        # Load the beautiful generated icon
        raw_icon = Image.open(icon_path)
        self.icon_image = ctk.CTkImage(light_image=raw_icon, dark_image=raw_icon, size=(120, 120))
        
        super().__init__(
            master, 
            corner_radius=CORNER_RADIUS,
            text=f"\n{title}\n\n{placeholder}",
            image=self.icon_image,
            compound="top", # Icon on top of text
            font=FONTS["body"],
            fg_color=ThemeManager.get_color("card_bg"),
            border_width=2,
            border_color=ThemeManager.get_color("border"),
            hover_color=ThemeManager.get_color("card_hover"),
            text_color=ThemeManager.get_color("text"),
            command=command,
            width=450,
            height=320,
            **kwargs
        )
        self.title_base = title
        self.placeholder_base = placeholder
        self.default_icon = self.icon_image
        self.preview_image = None

    def set_file(self, filename, is_video=False):
        if filename:
            name = os.path.basename(filename)
            if len(name) > 35:
                name = name[:32] + "..."
            
            self.configure(
                text=f"\n{self.title_base}\n\n{name}",
                border_color="#00E5FF",
                text_color="#00E5FF"
            )
            self._generate_preview(filename, is_video)
        else:
            self.configure(
                text=f"\n{self.title_base}\n\n{self.placeholder_base}",
                image=self.default_icon,
                border_color=ThemeManager.get_color("border"),
                text_color=ThemeManager.get_color("text")
            )

    def _generate_preview(self, filepath, is_video):
        try:
            temp_preview = os.path.join("temp", f"preview_{int(time.time())}.jpg")
            if not os.path.exists("temp"): os.makedirs("temp")

            if is_video:
                cmd = [
                    "ffmpeg", "-i", filepath,
                    "-ss", "00:00:01", "-vframes", "1",
                    "-vf", "scale=380:-1",
                    "-q:v", "4", temp_preview, "-y"
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                preview_path = temp_preview
            else:
                preview_path = filepath

            img = Image.open(preview_path)
            img.thumbnail((350, 220))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_image = ctk_img
            self.configure(image=ctk_img, text=f"\n{self.title_base}")

        except Exception as e:
            print(f"Preview error: {e}")

class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Give cards frame some space

        # 1. Welcome
        self.welcome_label = ctk.CTkLabel(self, text="Hoş Geldiniz", font=FONTS["title"])
        self.welcome_label.grid(row=0, column=0, padx=PADDING, pady=(10, 20), sticky="w")

        # 2. Media Cards Container
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, padx=PADDING, pady=10, sticky="nsew")
        self.cards_frame.grid_columnconfigure((0, 1), weight=1)
        self.cards_frame.grid_rowconfigure(0, weight=1)

        # Video Card
        self.video_card = MediaCard(
            self.cards_frame, 
            title="VİDEO YÜKLE", 
            placeholder="Kayıtlı video dosyası (MP4, MKV...)", 
            icon_path="src/gui/assets/video_icon.png", 
            command=self.select_video
        )
        self.video_card.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

        # Thumbnail Card
        self.thumb_card = MediaCard(
            self.cards_frame, 
            title="THUMBNAIL YÜKLE", 
            placeholder="Kapak fotoğrafı (JPG, PNG...)", 
            icon_path="src/gui/assets/thumb_icon.png", 
            command=self.select_thumbnail
        )
        self.thumb_card.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")

        # Internal state
        self.video_path = ""
        self.thumb_path = ""

        # 3. User Notes
        self.notes_label = ctk.CTkLabel(self, text="AI İÇİN ÖZEL TALİMATLAR", font=FONTS["header"])
        self.notes_label.grid(row=2, column=0, padx=PADDING, pady=(20, 5), sticky="w")
        
        self.notes_text = ctk.CTkTextbox(self, height=150, corner_radius=CORNER_RADIUS, font=FONTS["body"])
        self.notes_text.grid(row=3, column=0, padx=PADDING, pady=5, sticky="ew")
        
        # Placeholder Logic
        self.placeholder_text = "Örn: Teknolojik bir ton kullan, başlıkta mutlaka '2025' geçsin..."
        self.notes_text.insert("0.0", self.placeholder_text)
        self.notes_text.configure(text_color="gray")
        
        self.notes_text.bind("<FocusIn>", self._clear_placeholder)
        self.notes_text.bind("<FocusOut>", self._restore_placeholder)

        # 4. Action Button
        self.start_btn = ctk.CTkButton(
            self, text="OTOMASYONU BAŞLAT", height=60, 
            font=("Arial", 20, "bold"), fg_color="#00E5FF", text_color="black",
            hover_color="#00B8D4", corner_radius=CORNER_RADIUS,
            command=self.start_process
        )
        self.start_btn.grid(row=4, column=0, padx=PADDING, pady=(30, 20), sticky="ew")

    def _clear_placeholder(self, event):
        if self.notes_text.get("0.0", "end-1c") == self.placeholder_text:
            self.notes_text.delete("0.0", "end")
            self.notes_text.configure(text_color=("#1A1A1A", "#FFFFFF"))

    def _restore_placeholder(self, event):
        if not self.notes_text.get("0.0", "end-1c").strip():
            self.notes_text.delete("0.0", "end")
            self.notes_text.insert("0.0", self.placeholder_text)
            self.notes_text.configure(text_color="gray")

    def select_video(self):
        file = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Video Seçin",
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi")]
        )
        if file:
            self.video_path = file
            self.video_card.set_file(file, is_video=True)

    def select_thumbnail(self):
        file = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Kapak Fotoğrafı Seçin",
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file:
            self.thumb_path = file
            self.thumb_card.set_file(file, is_video=False)

    def start_process(self):
        if not self.video_path:
            from tkinter import messagebox
            messagebox.showwarning("Eksik Dosya", "Lütfen önce bir video dosyası seçin!")
            return
        
        # Extract notes (stripping placeholder if still there)
        notes = self.notes_text.get("0.0", "end-1c").strip()
        if notes == self.placeholder_text:
            notes = ""
            
        # Call bridge through app (app -> main_content_frame -> HomePage)
        # Structure is YouTubeAutomationApp (master.master) -> main_content_frame (master) -> HomePage
        self.master.master.show_process(self.video_path, self.thumb_path, notes)

