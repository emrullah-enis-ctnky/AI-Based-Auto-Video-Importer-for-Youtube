import customtkinter as ctk
from ..styles import PADDING, CORNER_RADIUS, FONTS
from tkinter import filedialog
import os

class MediaCard(ctk.CTkFrame):
    def __init__(self, master, title, placeholder, icon_char, command, **kwargs):
        super().__init__(master, corner_radius=CORNER_RADIUS, **kwargs)
        
        self.configure(fg_color=("gray90", "gray15"), border_width=2, border_color=("gray80", "gray25"))
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text=title, font=FONTS["header"])
        self.title_label.grid(row=0, column=0, pady=(15, 5))

        # Icon/Symbol area
        self.icon_label = ctk.CTkLabel(self, text=icon_char, font=("Inter", 64))
        self.icon_label.grid(row=1, column=0, pady=10)

        self.status_label = ctk.CTkLabel(self, text=placeholder, font=FONTS["small"], text_color="gray")
        self.status_label.grid(row=2, column=0, pady=(0, 15))

        # Absolute overlay button for click
        self.btn = ctk.CTkButton(
            self, text="", fg_color="transparent", hover_color=("gray80", "gray30"),
            command=command
        )
        self.btn.place(relx=0, rely=0, relwidth=1, relheight=1)

    def set_file(self, filename):
        if filename:
            name = os.path.basename(filename)
            if len(name) > 20:
                name = name[:17] + "..."
            self.status_label.configure(text=name, text_color="#00E5FF")
            self.configure(border_color="#00E5FF")
        else:
            self.status_label.configure(text="Dosya Seçilmedi", text_color="gray")
            self.configure(border_color=("gray80", "gray25"))

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
            placeholder="MP4, MKV, AVI", 
            icon_char="📹", 
            command=self.select_video
        )
        self.video_card.grid(row=0, column=0, padx=20, pady=10, sticky="nsew", ipadx=20, ipady=40)

        # Thumbnail Card
        self.thumb_card = MediaCard(
            self.cards_frame, 
            title="THUMBNAIL YÜKLE", 
            placeholder="JPG, PNG, JPEG", 
            icon_char="🖼️", 
            command=self.select_thumbnail
        )
        self.thumb_card.grid(row=0, column=1, padx=20, pady=10, sticky="nsew", ipadx=20, ipady=40)

        # Internal state
        self.video_path = ""
        self.thumb_path = ""

        # 3. User Notes
        self.notes_label = ctk.CTkLabel(self, text="AI İÇİN ÖZEL TALİMATLAR", font=FONTS["header"])
        self.notes_label.grid(row=2, column=0, padx=PADDING, pady=(30, 10), sticky="w")
        
        self.notes_text = ctk.CTkTextbox(self, height=150, corner_radius=CORNER_RADIUS, font=FONTS["body"])
        self.notes_text.grid(row=3, column=0, padx=PADDING, pady=0, sticky="ew")
        self.notes_text.insert("0.0", "Örn: Teknolojik bir ton kullan, başlıkta mutlaka '2025' geçsin...")

        # 4. Action Button
        self.start_btn = ctk.CTkButton(
            self, text="OTOMASYONU BAŞLAT", height=60, 
            font=("Inter", 18, "bold"), fg_color="#00E5FF", text_color="black",
            hover_color="#00B8D4", corner_radius=CORNER_RADIUS,
            command=self.start_process
        )
        self.start_btn.grid(row=4, column=0, padx=PADDING, pady=40, sticky="ew")

    def select_video(self):
        file = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.avi")])
        if file:
            self.video_path = file
            self.video_card.set_file(file)

    def select_thumbnail(self):
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file:
            self.thumb_path = file
            self.thumb_card.set_file(file)

    def start_process(self):
        if not self.video_path:
            from tkinter import messagebox
            messagebox.showwarning("Eksik Dosya", "Lütfen önce bir video dosyası seçin!")
            return
        
        print(f"İşlem başlatılıyor: {os.path.basename(self.video_path)}")

