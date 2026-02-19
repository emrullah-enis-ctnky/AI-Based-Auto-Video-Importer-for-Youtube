import customtkinter as ctk

# Appearance Settings
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Color Palette Definitions
COLORS = {
    "dark": {
        "bg": "#0F0F0F",
        "sidebar": "#161616",
        "card_bg": "#1E222D",    # Deep Navy/Slate
        "card_hover": "#262C3D", # Lighter Navy
        "accent": "#00E5FF",  # Neon Cyan
        "text": "#FFFFFF",
        "secondary_text": "#AAAAAA",
        "success": "#00C853",
        "error": "#FF1744",
        "border": "#2D3447"
    },
    "light": {
        "bg": "#F5F7FA",
        "sidebar": "#FFFFFF",
        "card_bg": "#FFFFFF",
        "card_hover": "#F0F4F8",
        "accent": "#0D47A1",  # Darker Blue
        "text": "#202124",
        "secondary_text": "#5F6368",
        "success": "#1E8E3E",
        "error": "#D93025",
        "border": "#DADCE0"
    }
}

# Typography
FONTS = {
    "title": ("Arial", 38, "bold"),
    "header": ("Arial", 26, "bold"),
    "body": ("Arial", 18, "normal"),
    "small": ("Arial", 14, "normal"),
    "mono": ("Courier New", 16, "normal")
}

# Localization Data
TRANSLATIONS = {
    "tr": {
        "home": "Ana Sayfa",
        "settings": "Ayarlar",
        "app_title": "AI Destekli YouTube Video Yükleyici",
        "sidebar_toggle": "Sidebar'ı Daralt",
        "theme": "Tema:",
        "theme_system": "Sistem",
        "theme_light": "Açık",
        "theme_dark": "Koyu",
        "lang": "Dil:",
        "video_upload": "VİDEO YÜKLE",
        "thumb_upload": "THUMBNAIL YÜKLE",
        "video_desc": "Kayıtlı video dosyası (MP4, MKV...)",
        "thumb_desc": "Kapak fotoğrafı (JPG, PNG...)",
        "ai_notes": "AI İÇİN ÖZEL TALİMATLAR",
        "notes_placeholder": "Örn: Teknolojik bir ton kullan, başlıkta mutlaka '2025' geçsin...",
        "start_btn": "OTOMASYONU BAŞLAT",
        "processing": "Otomasyon Devam Ediyor",
        "ai_analysis": "AI İçerik Analizi",
        "yt_upload": "YouTube Yükleme",
        "logs_btn": "LOGLARI GÖSTER",
        "cancel_btn": "VAZGEÇ",
        "finish_btn": "BİTİR VE ANA SAYFAYA DÖN",
        "debug_mode": "Hata Ayıklama Modu (Debug)",
        "compression": "AI İçin Medya Sıkıştırma",
        "compression_info": "İpucu: Sıkıştırma sadece AI analizi için kullanılır. Video YouTube'a orijinal kalitesinde yüklenir.",
        "missing_video": "Lütfen önce bir video dosyası seçin!",
        "cancel_confirm": "İşlemi iptal etmek istediğinize emin misiniz?",
        "all_done": "✅ Tüm işlemler başarıyla tamamlandı!",
        "video_link": "🎬 Video Linki:",
        "system": "Sistem"
    },
    "en": {
        "home": "Home Page",
        "settings": "Settings",
        "app_title": "AI Powered YouTube Video Importer",
        "sidebar_toggle": "Collapse Sidebar",
        "theme": "Theme:",
        "theme_system": "System",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "lang": "Language:",
        "video_upload": "UPLOAD VIDEO",
        "thumb_upload": "UPLOAD THUMBNAIL",
        "video_desc": "Saved video file (MP4, MKV...)",
        "thumb_desc": "Cover photo (JPG, PNG...)",
        "ai_notes": "SPECIAL AI INSTRUCTIONS",
        "notes_placeholder": "E.g.: Use a tech tone, must include '2025' in title...",
        "start_btn": "START AUTOMATION",
        "processing": "Automation in Progress",
        "ai_analysis": "AI Content Analysis",
        "yt_upload": "YouTube Upload",
        "logs_btn": "SHOW LOGS",
        "cancel_btn": "CANCEL",
        "finish_btn": "FINISH AND RETURN HOME",
        "debug_mode": "Debug Mode",
        "compression": "Media Compression for AI",
        "compression_info": "Tip: Compression is only used for AI analysis. The video is uploaded to YouTube in its original quality.",
        "missing_video": "Please select a video file first!",
        "cancel_confirm": "Are you sure you want to cancel?",
        "all_done": "✅ All processes completed successfully!",
        "video_link": "🎬 Video Link:",
        "system": "System"
    }
}

class Localizer:
    _lang = "tr"
    
    @classmethod
    def set_language(cls, lang):
        if lang in TRANSLATIONS:
            cls._lang = lang
            
    @classmethod
    def translate(cls, key):
        return TRANSLATIONS[cls._lang].get(key, key)

class ThemeManager:
    @staticmethod
    def get_color(key):
        """Returns the appropriate color based on the current mode."""
        mode = ctk.get_appearance_mode().lower()
        if mode == "dark":
            return COLORS["dark"].get(key, "#FF00FF")
        return COLORS["light"].get(key, "#FF00FF")

    @staticmethod
    def get_tuple(key):
        """Returns a (light, dark) color tuple for dynamic switching."""
        return (COLORS["light"].get(key, "#FF00FF"), COLORS["dark"].get(key, "#FF00FF"))

# UI Constants
PADDING = 20
CORNER_RADIUS = 10
