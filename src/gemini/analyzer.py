import time
import json
import google.generativeai as genai
from .client import setup_gemini
from .prompts import SEO_PROMPT
from .models import VideoMetadata
from utils.logger import logger

def analyze_content(video_path, thumbnail_path, user_notes=""):
    """
    Analyzes video, thumbnail, and user notes to generate metadata.
    """
    model = setup_gemini()
    if not model:
        return None

    try:
        logger.info(f"Multimodal dosyalar yükleniyor...")
        
        # 1. Upload Video
        video_file = genai.upload_file(path=video_path)
        logger.info(f"Video yüklendi (File ID: {video_file.name}). İşleniyor...")

        # 2. Upload Thumbnail
        thumbnail_file = genai.upload_file(path=thumbnail_path)
        logger.info(f"Thumbnail yüklendi (File ID: {thumbnail_file.name}).")

        # 3. Wait for Video processing
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            video_file = genai.get_file(video_file.name)
            logger.debug("Video işleniyor...")

        if video_file.state.name == "FAILED":
            logger.error("Video işleme başarısız oldu.")
            return None

        logger.success("Tüm dosyalar hazır. AI Analizi başlatılıyor...")

        # 4. Prepare Prompt
        final_prompt = SEO_PROMPT.format(user_notes=user_notes if user_notes else "None provided.")

        # 5. Generate content with both video and thumbnail (with retry logic)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content([video_file, thumbnail_file, final_prompt])
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"AI Analiz denemesi {attempt+1} başarısız, tekrar deneniyor... ({str(e)})")
                    time.sleep(2)
                else:
                    raise e
        
        # 6. Parse JSON response
        try:
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            data = json.loads(content)
            
            metadata = VideoMetadata(
                title=data.get("title", "Başlıksız Video"),
                description=data.get("description", "Açıklama üretilemedi."),
                tags=data.get("tags", [])
            )
            
            # 7. Cleanup
            try:
                genai.delete_file(video_file.name)
                genai.delete_file(thumbnail_file.name)
                logger.debug("Google AI sunucusundaki geçici dosyalar silindi.")
            except Exception as e:
                logger.warning(f"Geçici dosyalar silinirken hata (limiti etkilemez): {str(e)}")
            
            return metadata
            
        except json.JSONDecodeError as e:
            logger.error(f"AI yanıtı JSON olarak ayrıştırılamadı: {str(e)}")
            logger.debug(f"Ham yanıt: {response.text}")
            return None

    except Exception as e:
        logger.error(f"Multimodal analiz hatası: {str(e)}")
        return None
