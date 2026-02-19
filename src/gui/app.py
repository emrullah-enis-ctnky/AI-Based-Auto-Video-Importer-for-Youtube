import customtkinter as ctk
from .styles import ThemeManager, PADDING, CORNER_RADIUS, FONTS
import os

class YouTubeAutomationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("AI-Powered YouTube Automation")
        self.geometry("1400x850") # Set starting size large
        self.minsize(1280, 720)   # Minimum resolution
        
        # Shared State (Settings)
        self.use_compression = ctk.BooleanVar(value=True)
        self.debug_mode = ctk.BooleanVar(value=False)
        
        # Grid Configuration (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="YouTube AI", 
            font=FONTS["title"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Sidebar Buttons
        self.home_button = ctk.CTkButton(
            self.sidebar_frame, corner_radius=CORNER_RADIUS, height=40, border_spacing=10, 
            text="Ana Sayfa", fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), anchor="w", command=self.show_home
        )
        self.home_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        self.settings_button = ctk.CTkButton(
            self.sidebar_frame, corner_radius=CORNER_RADIUS, height=40, border_spacing=10, 
            text="Ayarlar", fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), anchor="w", command=self.show_settings
        )
        self.settings_button.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        # Appearance Mode Selector
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=["System", "Light", "Dark"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # 2. Main Content Frame
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=0, column=1, sticky="nsew", padx=PADDING, pady=PADDING)
        
        # Initial Page
        self.show_home()

    def show_home(self):
        self._clear_main_content()
        from .pages.home import HomePage
        self.home_page = HomePage(self.main_content_frame, fg_color="transparent")
        self.home_page.pack(fill="both", expand=True)
        
        self.home_button.configure(fg_color=("gray75", "gray25"))
        self.settings_button.configure(fg_color="transparent")

    def show_settings(self):
        self._clear_main_content()
        from .pages.settings import SettingsPage
        self.settings_page = SettingsPage(
            self.main_content_frame, 
            fg_color="transparent",
            compression_var=self.use_compression,
            debug_var=self.debug_mode
        )
        self.settings_page.pack(fill="both", expand=True)
        self.settings_button.configure(fg_color=("gray75", "gray25"))
        self.home_button.configure(fg_color="transparent")

    def show_process(self, video_path, thumb_path, user_notes):
        self._clear_main_content()
        from .pages.process import ProcessPage
        self.process_page = ProcessPage(
            self.main_content_frame,
            video_path=video_path,
            thumb_path=thumb_path,
            user_notes=user_notes,
            use_compression=self.use_compression.get(),
            debug_mode=self.debug_mode.get(),
            fg_color="transparent"
        )
        self.process_page.pack(fill="both", expand=True)
        # Highlight nothing in sidebar during process? Or just keep home highlighted?
        self.home_button.configure(fg_color="transparent")
        self.settings_button.configure(fg_color="transparent")

    def _clear_main_content(self):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = YouTubeAutomationApp()
    app.mainloop()
