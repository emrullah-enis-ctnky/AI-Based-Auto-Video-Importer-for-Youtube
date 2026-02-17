import time
import json
import google.generativeai as genai
from .client import setup_gemini
from .prompts import SEO_PROMPT
from .models import VideoMetadata
from utils.logger import logger

def analyze_video(video_path):
    """
    Uploads a video to Google Generative AI and analyzes it to generate metadata.
    """
    model = setup_gemini()
    if not model:
        return None

    try:
        logger.info(f"Video yükleniyor: {video_path}")
        # 1. Upload the file
        video_file = genai.upload_file(path=video_path)
        logger.info(f"Yükleme tamamlandı, işleniyor (File ID: {video_file.name})...")

        # 2. Wait for processing
        while video_file.state.name == "PROCESSING":
            time.sleep(5)
            video_file = genai.get_file(video_file.name)
            logger.debug("İşleniyor...")

        if video_file.state.name == "FAILED":
            logger.error("Video işleme başarısız oldu.")
            return None

        logger.success("Video başarıyla işlendi. AI Analizi başlıyor...")

        # 3. Generate content
        response = model.generate_content([video_file, SEO_PROMPT])
        
        # 4. Parse JSON response
        try:
            # AI might wrap JSON in markdown blocks
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
            
            # 5. Cleanup (Optional but good practice)
            # genai.delete_file(video_file.name)
            
            return metadata
            
        except json.JSONDecodeError as e:
            logger.error(f"AI yanıtı JSON olarak ayrıştırılamadı: {str(e)}")
            logger.debug(f"Ham yanıt: {response.text}")
            return None

    except Exception as e:
        logger.error(f"Video analiz hatası: {str(e)}")
        return None
