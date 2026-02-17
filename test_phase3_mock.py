import sys
import os
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from gemini.models import VideoMetadata
from utils.logger import logger

def test_ai_display():
    """
    Mocks the AI response and verifies the display logic.
    """
    mock_metadata = VideoMetadata(
        title="Harika Bir Python Dersi 🚀",
        description="Bu videoda Python ile YouTube otomasyonu yapmayı öğreniyoruz. Abone olmayı unutmayın!",
        tags=["python", "otomasyon", "youtube", "ai", "gemini"]
    )
    
    logger.info("Mock AI verisi doğrulanıyor...")
    
    from rich.table import Table
    from utils.logger import console
    
    table = Table(title="Generate Edilen Metadata (MOCK TEST)", show_header=True, header_style="bold magenta")
    table.add_column("Alan", style="cyan", width=12)
    table.add_column("İçerik", style="white")
    
    table.add_row("Başlık", mock_metadata.title)
    table.add_row("Açıklama", mock_metadata.description)
    table.add_row("Etiketler", ", ".join(mock_metadata.tags))
    
    console.print(table)
    logger.success("UI Görüntüleme testi başarılı.")

if __name__ == "__main__":
    test_ai_display()
