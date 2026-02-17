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
        # Upgraded to Gemini 3 Flash (Latest frontier model)
        model = genai.GenerativeModel('gemini-3-flash-preview') 
        logger.debug("Gemini 3 Flash istemcisi başarıyla yapılandırıldı.")
        return model
    except Exception as e:
        logger.error(f"Gemini yapılandırması sırasında hata: {str(e)}")
        return None
