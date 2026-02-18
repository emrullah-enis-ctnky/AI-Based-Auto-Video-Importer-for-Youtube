import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from gemini.client import setup_gemini
from utils.logger import logger

def live_smoke_test():
    """
    Performs a real text-based request to Gemini to verify connectivity.
    """
    logger.banner("🔥 Gemini Live Smoke Test")
    
    model = setup_gemini()
    if not model:
        logger.error("Gemini istemcisi kurulamadı. API anahtarını kontrol edin.")
        return

    logger.info(f"Model: {model.model_name}")
    logger.info("Test mesajı gönderiliyor: 'Merhaba, nasılsın?'")
    
    try:
        response = model.generate_content("Merhaba, nasılsın? Çok kısa bir cevap ver.")
        logger.success("Gemini'den yanıt alındı!")
        logger.info(f"Yapay Zeka Yanıtı: {response.text.strip()}")
        logger.success("Canlı bağlantı testi BAŞARILI. ✅")
    except Exception as e:
        logger.error(f"Canlı bağlantı hatası: {str(e)}")
        if "404" in str(e):
            logger.warning("Not: Gemini 3 Flash şu an hesabınız veya bölgeniz için aktif olmayabilir. Model ismini 'gemini-1.5-flash' yaparak tekrar deneyebilirsiniz.")

if __name__ == "__main__":
    live_smoke_test()
