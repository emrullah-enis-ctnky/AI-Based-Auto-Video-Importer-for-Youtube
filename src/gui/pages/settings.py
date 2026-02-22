import customtkinter as ctk
from gui.styles import PADDING, CORNER_RADIUS, FONTS, Localizer
from utils.config import config

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, compression_var, debug_var, lang_var, **kwargs):
        super().__init__(master, **kwargs)
        self.lang_var = lang_var
        
        self.grid_columnconfigure(0, weight=1)
        
        # 1. Header
        self.header_label = ctk.CTkLabel(self, text=Localizer.translate("settings"), font=FONTS["title"])
        self.header_label.grid(row=0, column=0, padx=PADDING, pady=(10, 30), sticky="w")

        # 2. Settings Group
        self.settings_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray15"), corner_radius=CORNER_RADIUS)
        self.settings_frame.grid(row=1, column=0, padx=PADDING, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Language Selection row
        self.lang_row = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.lang_row.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.lang_row.grid_columnconfigure(0, weight=1)

        self.lang_label = ctk.CTkLabel(self.lang_row, text=Localizer.translate("lang"), font=FONTS["header"])
        self.lang_label.grid(row=0, column=0, sticky="w")
        
        # Determine initial selection display
        current_display = "Türkçe" if self.lang_var.get() == "tr" else "English"
        
        self.lang_menu = ctk.CTkOptionMenu(
            self.lang_row, values=["Türkçe", "English"],
            command=self.on_lang_change
        )
        self.lang_menu.set(current_display)
        self.lang_menu.grid(row=0, column=1, sticky="e")

        # Media Compression row
        self.comp_row = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.comp_row.grid(row=1, column=0, sticky="ew", padx=20, pady=15)
        self.comp_row.grid_columnconfigure(0, weight=1)

        self.comp_label = ctk.CTkLabel(self.comp_row, text=Localizer.translate("compression"), font=FONTS["header"])
        self.comp_label.grid(row=0, column=0, sticky="w")
        
        self.comp_switch = ctk.CTkSwitch(self.comp_row, text="", variable=compression_var)
        self.comp_switch.grid(row=0, column=1, sticky="e")

        self.comp_info_label = ctk.CTkLabel(
            self.settings_frame, 
            text=Localizer.translate("compression_info"), 
            font=FONTS["small"], 
            text_color="gray",
            wraplength=800,
            justify="left"
        )
        self.comp_info_label.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="w")

        # Debug Mode row
        self.debug_row = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        self.debug_row.grid(row=3, column=0, sticky="ew", padx=20, pady=15)
        self.debug_row.grid_columnconfigure(0, weight=1)

        self.debug_label = ctk.CTkLabel(self.debug_row, text=Localizer.translate("debug_mode"), font=FONTS["header"])
        self.debug_label.grid(row=0, column=0, sticky="w")
        
        self.debug_switch = ctk.CTkSwitch(self.debug_row, text="", variable=debug_var)
        self.debug_switch.grid(row=0, column=1, sticky="e")

        # 3. Account Management
        self.account_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.account_frame.grid(row=2, column=0, padx=PADDING, pady=20, sticky="ew")
        
        self.logout_btn = ctk.CTkButton(
            self.account_frame, 
            text=Localizer.translate("logout_btn"),
            fg_color="#D93025", # Error/Red color for destructive action
            hover_color="#B71C1C",
            height=45,
            font=FONTS["body"],
            command=self.on_logout
        )
        self.logout_btn.pack(pady=10)

        self.info_label = ctk.CTkLabel(
            self, text="v1.1.0 - AI-Powered Auto Video Importer", 
            font=FONTS["small"], text_color="gray"
        )
        self.info_label.grid(row=10, column=0, pady=40)

    def on_lang_change(self, val):
        self.winfo_toplevel().change_language(val)

    def on_logout(self):
        from tkinter import messagebox
        import os
        
        # Confirm with user
        if messagebox.askyesno(
            Localizer.translate("logout_btn"), 
            Localizer.translate("logout_confirm")
        ):
            token_file = config.TOKEN_FILE
            if os.path.exists(token_file):
                try:
                    os.remove(token_file)
                    messagebox.showinfo("Başarılı" if Localizer._lang == "tr" else "Success", 
                                      "Oturum kapatıldı." if Localizer._lang == "tr" else "Logged out.")
                except Exception as e:
                    messagebox.showerror("Hata" if Localizer._lang == "tr" else "Error", str(e))
            else:
                messagebox.showinfo("Bilgi" if Localizer._lang == "tr" else "Info", 
                                  "Zaten açık bir oturum yok." if Localizer._lang == "tr" else "No active session found.")

    def refresh_localization(self):
        self.header_label.configure(text=Localizer.translate("settings"))
        self.lang_label.configure(text=Localizer.translate("lang"))
        self.comp_label.configure(text=Localizer.translate("compression"))
        self.comp_info_label.configure(text=Localizer.translate("compression_info"))
        self.debug_label.configure(text=Localizer.translate("debug_mode"))
        if hasattr(self, 'logout_btn'):
            self.logout_btn.configure(text=Localizer.translate("logout_btn"))
