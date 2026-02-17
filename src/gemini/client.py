import google.generativeai as genai
import os
from utils.config import config
from utils.logger import logger

def setup_gemini():
    """
    Configures the Gemini API with the provided API key.
    """
    api_key = config.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY eksik. Lütfen .env dosyasını kontrol edin.")
        return None
        
    try:
        genai.configure(api_key=api_key)
        # Use Gemini 1.5 Flash for faster and cost-effective video analysis
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.debug("Gemini istemcisi başarıyla yapılandırıldı.")
        return model
    except Exception as e:
        logger.error(f"Gemini yapılandırması sırasında hata: {str(e)}")
        return None
