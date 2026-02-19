import customtkinter as ctk
from ..styles import PADDING, CORNER_RADIUS, FONTS
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess
import time

class MediaCard(ctk.CTkFrame):
    def __init__(self, master, title, placeholder, icon_char, command, **kwargs):
        super().__init__(master, corner_radius=CORNER_RADIUS, **kwargs)
        
        self.configure(fg_color=("gray90", "gray15"), border_width=2, border_color=("gray80", "gray25"))
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text=title, font=FONTS["header"])
        self.title_label.grid(row=0, column=0, pady=(15, 5))

        # Media Preview Area
        self.preview_container = ctk.CTkFrame(self, fg_color="transparent")
        self.preview_container.grid(row=1, column=0, pady=10, sticky="nsew")
        self.preview_container.grid_columnconfigure(0, weight=1)
        self.preview_container.grid_rowconfigure(0, weight=1)

        # Icon/Symbol (Default)
        self.icon_label = ctk.CTkLabel(self.preview_container, text=icon_char, font=("Inter", 80))
        self.icon_label.grid(row=0, column=0)

        # File Status
        self.status_label = ctk.CTkLabel(self, text=placeholder, font=FONTS["small"], text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(0, 15))

        # Absolute overlay button for click
        self.btn = ctk.CTkButton(
            self, text="", fg_color="transparent", hover_color=("gray80", "gray30"),
            command=command
        )
        self.btn.place(relx=0, rely=0, relwidth=1, relheight=1)

    def set_file(self, filename, is_video=False):
        if filename:
            name = os.path.basename(filename)
            if len(name) > 25:
                name = name[:22] + "..."
            self.status_label.configure(text=name, text_color="#00E5FF")
            self.configure(border_color="#00E5FF")
            
            # Create Preview
            self._generate_preview(filename, is_video)
        else:
            self.status_label.configure(text="Dosya Seçilmedi", text_color="gray")
            self.configure(border_color=("gray80", "gray25"))
            self.icon_label.grid(row=0, column=0) # Show icon again

    def _generate_preview(self, filepath, is_video):
        try:
            temp_preview = os.path.join("temp", f"preview_{int(time.time())}.jpg")
            
            if is_video:
                # Extract middle frame using ffmpeg
                cmd = [
                    "ffmpeg", "-i", filepath,
                    "-ss", "00:00:01", "-vframes", "1",
                    "-q:v", "2", temp_preview, "-y"
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                preview_path = temp_preview
            else:
                preview_path = filepath

            # Load and show image
            img = Image.open(preview_path)
            # Maintain aspect ratio for the card (approx 200x150)
            img.thumbnail((250, 180))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # Remove old icon and show image
            self.icon_label.grid_forget()
            if hasattr(self, "img_label"):
                self.img_label.destroy()
                
            self.img_label = ctk.CTkLabel(self.preview_container, image=ctk_img, text="")
            self.img_label.grid(row=0, column=0)
            
            # Store reference to prevent GC
            self.img_label.image = ctk_img

        except Exception as e:
            print(f"Preview generation error: {e}")

class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1) # Spacer

        # 1. Welcome
        self.welcome_label = ctk.CTkLabel(self, text="Hoş Geldiniz", font=FONTS["title"])
        self.welcome_label.grid(row=0, column=0, padx=PADDING, pady=(10, 30), sticky="w")

        # 2. Media Cards Container
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, padx=PADDING, pady=10, sticky="nsew")
        self.cards_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        # Video Card
        self.video_card = MediaCard(
            self.cards_frame, 
            title="VİDEO YÜKLE", 
            placeholder="Kayıtlı video dosyası (MP4, MKV...)", 
            icon_char="📤", # Improved upload icon
            command=self.select_video
        )
        self.video_card.grid(row=0, column=0, padx=20, pady=10, sticky="nsew", ipadx=20, ipady=40)

        # Thumbnail Card
        self.thumb_card = MediaCard(
            self.cards_frame, 
            title="THUMBNAIL YÜKLE", 
            placeholder="Kapak fotoğrafı (JPG, PNG...)", 
            icon_char="📷", 
            command=self.select_thumbnail
        )
        self.thumb_card.grid(row=0, column=1, padx=20, pady=10, sticky="nsew", ipadx=20, ipady=40)

        # Internal state
        self.video_path = ""
        self.thumb_path = ""

        # 3. User Notes
        self.notes_label = ctk.CTkLabel(self, text="AI İÇİN ÖZEL TALİMATLAR", font=FONTS["header"])
        self.notes_label.grid(row=2, column=0, padx=PADDING, pady=(30, 10), sticky="w")
        
        self.notes_text = ctk.CTkTextbox(self, height=180, corner_radius=CORNER_RADIUS, font=FONTS["body"])
        self.notes_text.grid(row=3, column=0, padx=PADDING, pady=0, sticky="ew")
        
        # Simulated Placeholder logic
        # (CustomTkinter Textbox doesn't have placeholder_text)
        self.placeholder_text = "Örn: Teknolojik bir ton kullan, başlıkta mutlaka '2025' geçsin..."
        self.notes_text.insert("0.0", self.placeholder_text)
        self.notes_text.tag_add("placeholder", "0.0", "end")
        self.notes_text.tag_config("placeholder", foreground="gray")
        
        self.notes_text.bind("<FocusIn>", self._clear_placeholder)
        self.notes_text.bind("<FocusOut>", self._restore_placeholder)

        # 4. Action Button
        self.start_btn = ctk.CTkButton(
            self, text="OTOMASYONU BAŞLAT", height=70, 
            font=("Inter", 20, "bold"), fg_color="#00E5FF", text_color="black",
            hover_color="#00B8D4", corner_radius=CORNER_RADIUS,
            command=self.start_process
        )
        self.start_btn.grid(row=4, column=0, padx=PADDING, pady=50, sticky="ew")

    def _clear_placeholder(self, event):
        if self.notes_text.get("0.0", "end-1c") == self.placeholder_text:
            self.notes_text.delete("0.0", "end")
            # Use appropriate text color based on theme
            self.notes_text.configure(text_color=ctk.ThemeManager.theme["CTkTextbox"]["text_color"])

    def _restore_placeholder(self, event):
        if not self.notes_text.get("0.0", "end-1c").strip():
            self.notes_text.delete("0.0", "end")
            self.notes_text.insert("0.0", self.placeholder_text)
            self.notes_text.configure(text_color="gray")

    def select_video(self):
        file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
        if file:
            self.video_path = file
            self.video_card.set_file(file, is_video=True)

    def select_thumbnail(self):
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file:
            self.thumb_path = file
            self.thumb_card.set_file(file, is_video=False)

    def start_process(self):
        if not self.video_path:
            from tkinter import messagebox
            messagebox.showwarning("Eksik Dosya", "Lütfen önce bir video dosyası seçin!")
            return
        
        print(f"İşlem başlatılıyor: {os.path.basename(self.video_path)}")

