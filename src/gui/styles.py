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
    "title": ("Arial", 38, "bold"),
    "header": ("Arial", 26, "bold"),
    "body": ("Arial", 18, "normal"),
    "small": ("Arial", 14, "normal"),
    "mono": ("Courier New", 16, "normal")
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
