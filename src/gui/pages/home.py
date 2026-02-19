import customtkinter as ctk
from gui.styles import PADDING, CORNER_RADIUS, FONTS, ThemeManager, Localizer, get_resource_path
from tkinter import filedialog
from PIL import Image
import os
import subprocess
import time

class MediaCard(ctk.CTkButton):
    def __init__(self, master, trans_key_title, trans_key_placeholder, icon_path, command, **kwargs):
        self.trans_key_title = trans_key_title
        self.trans_key_placeholder = trans_key_placeholder
        
        # Load the beautiful generated icon
        raw_icon = Image.open(icon_path)
        self.icon_image = ctk.CTkImage(light_image=raw_icon, dark_image=raw_icon, size=(120, 120))
        
        super().__init__(
            master, 
            corner_radius=CORNER_RADIUS,
            text=f"\n{Localizer.translate(trans_key_title)}\n\n{Localizer.translate(trans_key_placeholder)}",
            image=self.icon_image,
            compound="top", # Icon on top of text
            font=FONTS["body"],
            fg_color=ThemeManager.get_tuple("card_bg"),
            border_width=2,
            border_color=ThemeManager.get_tuple("border"),
            hover_color=ThemeManager.get_tuple("card_hover"),
            text_color=ThemeManager.get_tuple("text"),
            command=command,
            width=450,
            height=320,
            **kwargs
        )
        self.default_icon = self.icon_image
        self.preview_image = None
        self.current_filename = None

    def set_file(self, filename, is_video=False):
        if filename:
            self.current_filename = os.path.basename(filename)
            name = self.current_filename
            if len(name) > 35:
                name = name[:32] + "..."
            
            self.configure(
                text=f"\n{Localizer.translate(self.trans_key_title)}\n\n{name}",
                border_color="#00E5FF", # Neon Cyan is fine for both? Or maybe darker for light?
                text_color=("#002171", "#00E5FF") # Deep Navy for light, Neon Cyan for dark
            )
            self._generate_preview(filename, is_video)
        else:
            self.current_filename = None
            self.configure(
                text=f"\n{Localizer.translate(self.trans_key_title)}\n\n{Localizer.translate(self.trans_key_placeholder)}",
                image=self.default_icon,
                border_color=ThemeManager.get_tuple("border"),
                text_color=ThemeManager.get_tuple("text")
            )

    def refresh_localization(self):
        if not self.current_filename:
            self.configure(text=f"\n{Localizer.translate(self.trans_key_title)}\n\n{Localizer.translate(self.trans_key_placeholder)}")
        else:
            name = self.current_filename
            if len(name) > 35:
                name = name[:32] + "..."
            self.configure(text=f"\n{Localizer.translate(self.trans_key_title)}\n\n{name}")

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
            self.configure(image=ctk_img, text=f"\n{Localizer.translate(self.trans_key_title)}")

        except Exception as e:
            print(f"Preview error: {e}")

class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Give cards frame some space

        # 1. Welcome Header
        self.header_container = ctk.CTkFrame(self, fg_color="transparent")
        self.header_container.grid(row=0, column=0, padx=PADDING, pady=(20, 30), sticky="ew")
        self.header_container.grid_columnconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(
            self.header_container, 
            text=Localizer.translate("app_title"), 
            font=FONTS["title"],
            text_color=ThemeManager.get_tuple("accent")
        )
        self.welcome_label.grid(row=0, column=0)

        # 2. Media Cards Container
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, padx=PADDING, pady=10, sticky="nsew")
        self.cards_frame.grid_columnconfigure((0, 1), weight=1)
        self.cards_frame.grid_rowconfigure(0, weight=1)

        # Video Card
        from ..styles import get_resource_path
        self.video_card = MediaCard(
            self.cards_frame, 
            trans_key_title="video_upload", 
            trans_key_placeholder="video_desc", 
            icon_path=get_resource_path(os.path.join("src", "gui", "assets", "video_icon.png")), 
            command=self.select_video
        )
        self.video_card.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

        # Thumbnail Card
        self.thumb_card = MediaCard(
            self.cards_frame, 
            trans_key_title="thumb_upload", 
            trans_key_placeholder="thumb_desc", 
            icon_path=get_resource_path(os.path.join("src", "gui", "assets", "thumb_icon.png")), 
            command=self.select_thumbnail
        )
        self.thumb_card.grid(row=0, column=1, padx=15, pady=10, sticky="nsew")

        # Internal state
        self.video_path = ""
        self.thumb_path = ""

        # 3. User Notes
        self.notes_label = ctk.CTkLabel(self, text=Localizer.translate("ai_notes"), font=FONTS["header"])
        self.notes_label.grid(row=2, column=0, padx=PADDING, pady=(20, 5), sticky="w")
        
        self.notes_text = ctk.CTkTextbox(self, height=150, corner_radius=CORNER_RADIUS, font=FONTS["body"])
        self.notes_text.grid(row=3, column=0, padx=PADDING, pady=5, sticky="ew")
        
        # Placeholder Logic
        self.placeholder_text = Localizer.translate("notes_placeholder")
        self.notes_text.insert("0.0", self.placeholder_text)
        self.notes_text.configure(text_color="gray")
        
        self.notes_text.bind("<FocusIn>", self._clear_placeholder)
        self.notes_text.bind("<FocusOut>", self._restore_placeholder)

        # 4. Action Button
        self.start_btn = ctk.CTkButton(
            self, text=Localizer.translate("start_btn"), height=60, 
            font=("Arial", 20, "bold"), 
            fg_color=("#002171", "#00E5FF"), 
            text_color=("white", "black"),
            hover_color=("#00154B", "#00B8D4"), corner_radius=CORNER_RADIUS,
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

    def refresh_localization(self):
        self.welcome_label.configure(text=Localizer.translate("app_title"))
        self.notes_label.configure(text=Localizer.translate("ai_notes"))
        self.video_card.refresh_localization()
        self.thumb_card.refresh_localization()
        self.start_btn.configure(text=Localizer.translate("start_btn"))

    def select_video(self):
        file = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title=Localizer.translate("video_upload"),
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi")]
        )
        if file:
            self.video_path = file
            self.video_card.set_file(file, is_video=True)

    def select_thumbnail(self):
        file = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title=Localizer.translate("thumb_upload"),
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if file:
            self.thumb_path = file
            self.thumb_card.set_file(file, is_video=False)

    def start_process(self):
        if not self.video_path:
            from tkinter import messagebox
            messagebox.showwarning(Localizer.translate("missing_video"), Localizer.translate("missing_video"))
            return
        
        # Extract notes (stripping placeholder if still there)
        notes = self.notes_text.get("0.0", "end-1c").strip()
        if notes == self.placeholder_text:
            notes = ""
            
        # Call bridge through app (app -> main_content_frame -> HomePage)
        # Structure is YouTubeAutomationApp (master.master) -> main_content_frame (master) -> HomePage
        self.master.master.show_process(self.video_path, self.thumb_path, notes)

