import os
from googleapiclient.http import MediaFileUpload
from utils.logger import logger

def set_thumbnail(youtube, video_id, thumbnail_path):
    """
    Sets a custom thumbnail for a YouTube video.
    """
    if not thumbnail_path or not os.path.exists(thumbnail_path):
        logger.warning(f"Thumbnail dosyası bulunamadı veya belirtilmedi: {thumbnail_path}")
        return False

    logger.info(f"Kapak fotoğrafı yükleniyor: {thumbnail_path}")
    
    try:
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path)
        )
        response = request.execute()
        logger.success("Kapak fotoğrafı başarıyla ayarlandı.")
        return True
    except Exception as e:
        logger.error(f"Kapak fotoğrafı ayarlanırken hata: {str(e)}")
        return False
