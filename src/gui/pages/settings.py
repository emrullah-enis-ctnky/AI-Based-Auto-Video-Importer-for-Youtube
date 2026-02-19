import customtkinter as ctk
from ..styles import PADDING, CORNER_RADIUS, FONTS

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, compression_var, debug_var, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Uygulama Ayarları", font=FONTS["header"])
        self.title_label.grid(row=0, column=0, padx=PADDING, pady=(0, 20), sticky="w")

        # AI Settings Group
        self.ai_group = ctk.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.ai_group.grid(row=1, column=0, padx=PADDING, pady=10, sticky="ew")
        self.ai_group.grid_columnconfigure(0, weight=1)

        self.ai_label = ctk.CTkLabel(self.ai_group, text="AI Optimizasyon", font=FONTS["body"], text_color="#00E5FF")
        self.ai_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.compression_switch = ctk.CTkSwitch(
            self.ai_group, text="Hızlı AI Analizi (Video Sıkıştırma)", 
            variable=compression_var,
            font=FONTS["body"]
        )
        self.compression_switch.grid(row=1, column=0, padx=40, pady=10, sticky="w")
        
        self.comp_desc = ctk.CTkLabel(
            self.ai_group, 
            text="Analiz öncesi videoyu geçici olarak küçültür. YouTube kalitesini etkilemez.",
            font=FONTS["small"], text_color="gray"
        )
        self.comp_desc.grid(row=2, column=0, padx=40, pady=(0, 15), sticky="w")

        # System Settings Group
        self.sys_group = ctk.CTkFrame(self, corner_radius=CORNER_RADIUS)
        self.sys_group.grid(row=2, column=0, padx=PADDING, pady=10, sticky="ew")
        self.sys_group.grid_columnconfigure(0, weight=1)

        self.sys_label = ctk.CTkLabel(self.sys_group, text="Sistem ve Debug", font=FONTS["body"], text_color="#00E5FF")
        self.sys_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        self.debug_switch = ctk.CTkSwitch(
            self.sys_group, text="Gelişmiş Debug Modu", 
            variable=debug_var,
            font=FONTS["body"]
        )
        self.debug_switch.grid(row=1, column=0, padx=40, pady=15, sticky="w")

        self.info_label = ctk.CTkLabel(
            self, text="v1.0.0 - AI-Powered Auto Video Importer", 
            font=FONTS["small"], text_color="gray"
        )
        self.info_label.grid(row=10, column=0, pady=40)
