import customtkinter as ctk
from .styles import ThemeManager, PADDING, CORNER_RADIUS, FONTS, Localizer
import os
import sys
import locale

# Add src to path to allow absolute imports from within src
sys.path.append(os.path.join(os.getcwd(), 'src'))

class YouTubeAutomationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 0. Language Detection
        try:
            # getlocale() returns (language code, encoding) e.g. ('en_US', 'UTF-8')
            sys_lang_tuple = locale.getlocale()
            sys_lang = sys_lang_tuple[0] if sys_lang_tuple else None
            curr_lang = "tr" if sys_lang and "tr" in sys_lang.lower() else "en"
        except Exception:
            curr_lang = "en"
        
        Localizer.set_language(curr_lang)
        self.language = ctk.StringVar(value=curr_lang)

        # Window Configuration
        self.title(Localizer.translate("app_title"))
        self.geometry("1400x850") 
        self.minsize(1280, 720) 

        # Set Application Icon
        try:
            from PIL import Image
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                # On Linux, iconphoto with PhotoImage is best
                from tkinter import PhotoImage
                import tkinter as tk
                # Convert PIL to PhotoImage
                from PIL import ImageTk
                icon_img = ImageTk.PhotoImage(img)
                self.wm_iconphoto(True, icon_img)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        self.sidebar_visible = True

        # Shared State (Settings)
        self.use_compression = ctk.BooleanVar(value=True)
        self.debug_mode = ctk.BooleanVar(value=False)
        
        # Main Layout: 
        # Column 0: Sidebar (can be toggled)
        # Column 1: Main Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # 1. Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Spacer

        # Sidebar Buttons
        self.home_button = ctk.CTkButton(
            self.sidebar_frame, corner_radius=CORNER_RADIUS, height=45, border_spacing=10, 
            text=Localizer.translate("home"), fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), anchor="w", font=FONTS["body"], 
            command=self.show_home
        )
        self.home_button.grid(row=0, column=0, sticky="ew", padx=10, pady=(30, 5))

        self.settings_button = ctk.CTkButton(
            self.sidebar_frame, corner_radius=CORNER_RADIUS, height=45, border_spacing=10, 
            text=Localizer.translate("settings"), fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), anchor="w", font=FONTS["body"], 
            command=self.show_settings
        )
        self.settings_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        # Toggle Button (Bottom of buttons, before spacer)
        self.toggle_btn = ctk.CTkButton(
            self.sidebar_frame, text="◀", width=30, height=30, 
            fg_color="transparent", text_color="gray", hover_color=("gray85", "gray25"),
            command=self.toggle_sidebar
        )
        self.toggle_btn.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        # Appearance Mode Selector
        self.appearance_mode_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.appearance_mode_frame.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        self.appearance_mode_label = ctk.CTkLabel(self.appearance_mode_frame, text=Localizer.translate("theme"), anchor="w", font=FONTS["small"])
        self.appearance_mode_label.pack(side="top", fill="x")
        
        self.theme_options = [
            Localizer.translate("theme_system"),
            Localizer.translate("theme_light"),
            Localizer.translate("theme_dark")
        ]
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.appearance_mode_frame, 
            values=self.theme_options,
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.pack(side="top", fill="x", pady=(5, 0))
        
        # Set current selection localized
        curr = ctk.get_appearance_mode()
        if curr == "System": self.appearance_mode_menu.set(Localizer.translate("theme_system"))
        elif curr == "Light": self.appearance_mode_menu.set(Localizer.translate("theme_light"))
        elif curr == "Dark": self.appearance_mode_menu.set(Localizer.translate("theme_dark"))

        # 2. Main Content Frame
        self.main_content_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content_container.grid(row=0, column=1, sticky="nsew")
        self.main_content_container.grid_columnconfigure(0, weight=1)
        self.main_content_container.grid_rowconfigure(1, weight=1)

        # Top Bar for Toggle Button when sidebar is hidden
        self.top_bar = ctk.CTkFrame(self.main_content_container, height=40, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.expand_btn = ctk.CTkButton(
            self.top_bar, text="▶", width=30, height=30, 
            fg_color="transparent", text_color="gray", hover_color=("gray85", "gray25"),
            command=self.toggle_sidebar
        )
        self.expand_btn.grid(row=0, column=0, sticky="w")
        
        # DEFAULT CLOSED Sidebar logic
        self.sidebar_visible = False
        self.sidebar_frame.grid_remove()
        self.expand_btn.grid()

        self.main_content_frame = ctk.CTkFrame(self.main_content_container, corner_radius=0, fg_color="transparent")
        self.main_content_frame.grid(row=1, column=0, sticky="nsew", padx=PADDING, pady=(0, PADDING))
        
        # Initial Page
        self.show_home()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_remove()
            self.expand_btn.grid()
            self.sidebar_visible = False
        else:
            self.sidebar_frame.grid()
            self.expand_btn.grid_remove()
            self.sidebar_visible = True

    def refresh_ui(self):
        """Update sidebar and logo for language changes."""
        self.title(Localizer.translate("app_title"))
        self.home_button.configure(text=Localizer.translate("home"))
        self.settings_button.configure(text=Localizer.translate("settings"))
        self.appearance_mode_label.configure(text=Localizer.translate("theme"))
        
        # Refresh Theme Menu values
        self.theme_options = [
            Localizer.translate("theme_system"),
            Localizer.translate("theme_light"),
            Localizer.translate("theme_dark")
        ]
        self.appearance_mode_menu.configure(values=self.theme_options)
        
        # Keep current selection localized
        curr = ctk.get_appearance_mode() # "System", "Light", "Dark"
        if curr == "System": self.appearance_mode_menu.set(Localizer.translate("theme_system"))
        elif curr == "Light": self.appearance_mode_menu.set(Localizer.translate("theme_light"))
        elif curr == "Dark": self.appearance_mode_menu.set(Localizer.translate("theme_dark"))

        # Refresh current page
        for widget in self.main_content_frame.winfo_children():
            if hasattr(widget, 'refresh_localization'):
                widget.refresh_localization()

    def change_language(self, new_lang_val):
        # Map "Türkçe" -> "tr", "English" -> "en"
        lang_code = "tr" if "türkçe" in new_lang_val.lower() else "en"
        Localizer.set_language(lang_code)
        self.refresh_ui()

    def show_home(self):
        self._clear_main_content()
        from .pages.home import HomePage
        self.home_page = HomePage(self.main_content_frame, fg_color="transparent")
        self.home_page.pack(fill="both", expand=True)
        
        # Use tuples for automatic (Light, Dark) mode switching
        from .styles import COLORS
        accent_tuple = (COLORS["light"]["accent"], COLORS["dark"]["accent"])
        text_tuple = ("white", "black") # White on deep navy, Black on neon cyan
        
        self.home_button.configure(fg_color=accent_tuple, text_color=text_tuple)
        self.settings_button.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def show_settings(self):
        self._clear_main_content()
        from .pages.settings import SettingsPage
        self.settings_page = SettingsPage(
            self.main_content_frame, 
            fg_color="transparent",
            compression_var=self.use_compression,
            debug_var=self.debug_mode,
            lang_var=self.language
        )
        self.settings_page.pack(fill="both", expand=True)
        
        from .styles import COLORS
        accent_tuple = (COLORS["light"]["accent"], COLORS["dark"]["accent"])
        text_tuple = ("white", "black")

        self.settings_button.configure(fg_color=accent_tuple, text_color=text_tuple)
        self.home_button.configure(fg_color="transparent", text_color=("gray10", "gray90"))

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

    def change_appearance_mode(self, new_mode_localized: str):
        # Map localized names back to standard ones
        if new_mode_localized == Localizer.translate("theme_system"): mode = "System"
        elif new_mode_localized == Localizer.translate("theme_light"): mode = "Light"
        elif new_mode_localized == Localizer.translate("theme_dark"): mode = "Dark"
        else: mode = "System"
        
        ctk.set_appearance_mode(mode)

if __name__ == "__main__":
    app = YouTubeAutomationApp()
    app.mainloop()
