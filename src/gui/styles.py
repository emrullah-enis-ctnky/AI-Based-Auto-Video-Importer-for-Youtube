import customtkinter as ctk

# Appearance Settings
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Color Palette Definitions
COLORS = {
    "dark": {
        "bg": "#1A1A1A",
        "sidebar": "#121212",
        "accent": "#00E5FF",  # Neon Cyan
        "text": "#FFFFFF",
        "secondary_text": "#AAAAAA",
        "success": "#00C853",
        "error": "#FF1744",
        "border": "#2C2C2C"
    },
    "light": {
        "bg": "#F5F5F5",
        "sidebar": "#FFFFFF",
        "accent": "#1A73E8",  # Google Blue
        "text": "#202124",
        "secondary_text": "#5F6368",
        "success": "#1E8E3E",
        "error": "#D93025",
        "border": "#DADCE0"
    }
}

# Typography
FONTS = {
    "title": ("Inter", 32, "bold"),
    "header": ("Inter", 22, "bold"),
    "body": ("Inter", 16, "normal"),
    "small": ("Inter", 13, "normal"),
    "mono": ("Consolas", 14, "normal")
}

class ThemeManager:
    @staticmethod
    def get_color(key):
        """Returns the appropriate color based on the current mode."""
        mode = ctk.get_appearance_mode().lower()
        if mode == "dark":
            return COLORS["dark"].get(key, "#FF00FF")
        return COLORS["light"].get(key, "#FF00FF")

# UI Constants
PADDING = 20
CORNER_RADIUS = 10
