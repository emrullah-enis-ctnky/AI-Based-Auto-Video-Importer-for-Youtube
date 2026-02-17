import logging
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

# Define a custom theme for our application
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green bold",
    "debug": "grey50",
    "banner": "magenta bold",
})

console = Console(theme=custom_theme)

class AppLogger:
    """
    Custom logger that provides concise, stylish terminal output (via Rich) 
    and detailed file output (via logging).
    """
    def __init__(self, name="AI_YouTube_Commiter"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Avoid duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        log_dir = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, "app.log")

        # 1. File Handler (Detailed - for debugging)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # 2. Rich Handler (Stylish Console)
        # We skip the standard console handler and use Rich's Console directly for more control
        self.logger.addHandler(file_handler)

    def banner(self, title):
        """Displays a stylish banner in the terminal."""
        banner_text = Text(title, style="banner", justify="center")
        console.print(Panel(banner_text, border_style="magenta", padding=(1, 2)))

    def debug(self, msg):
        self.logger.debug(msg)
        # We don't print debug to console by default to keep it clean

    def info(self, msg):
        self.logger.info(msg)
        console.print(f"[info]ℹ[/info] {msg}", style="info")

    def warning(self, msg):
        self.logger.warning(msg)
        console.print(f"[warning]⚠️ [/warning] {msg}", style="warning")

    def error(self, msg, exc_info=True):
        self.logger.error(msg, exc_info=exc_info)
        console.print(Panel(f"[error]ERROR:[/error] {msg}", border_style="red"))

    def success(self, msg):
        self.logger.info(msg)
        console.print(f"[success]✅[/success] {msg}", style="success")
    
    def step(self, step_num, msg):
        """Displays a formatted step message."""
        self.logger.info(f"Step {step_num}: {msg}")
        console.print(f"\n[banner]Step {step_num}:[/banner] [bold cyan]{msg}[/bold cyan]")

# Global instance
logger = AppLogger()
