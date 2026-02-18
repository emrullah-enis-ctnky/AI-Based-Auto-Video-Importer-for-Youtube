import os
import time
from googleapiclient.http import MediaFileUpload
from utils.logger import logger, console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn

def upload_video(youtube, video_path, metadata):
    """
    Uploads a video to YouTube with the provided metadata.
    Uses resumable (chunked) upload for stability.
    """
    logger.info(f"Video yükleme başlatılıyor: {video_path}")
    
    body = {
        'snippet': {
            'title': metadata.title,
            'description': metadata.description,
            'tags': metadata.tags,
            'categoryId': '22'  # '22' is People & Blogs. Can be made dynamic later.
        },
        'status': {
            'privacyStatus': 'private',  # Always upload as private first for safety
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(
        video_path,
        mimetype='video/*',
        resumable=True,
        chunksize=1024 * 1024  # 1MB chunks
    )

    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    video_id = None
    max_retries = 5
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Yükleniyor...", total=os.path.getsize(video_path))
        
        while video_id is None:
            attempt = 0
            while attempt < max_retries:
                try:
                    status, response = request.next_chunk()
                    break
                except Exception as e:
                    attempt += 1
                    if attempt < max_retries:
                        logger.warning(f"Yükleme hatası, tekrar deneniyor ({attempt}/{max_retries})...")
                        time.sleep(2 ** attempt) # Exponential backoff
                    else:
                        logger.error(f"Yükleme başarısız oldu: {str(e)}")
                        return None

            if status:
                progress.update(task, completed=status.resumable_progress)
            if response is not None:
                if 'id' in response:
                    video_id = response['id']
                    progress.update(task, completed=os.path.getsize(video_path))
                    logger.success(f"Video başarıyla yüklendi! Video ID: {video_id}")
                else:
                    logger.error(f"Yükleme tamamlandı ama Video ID alınamadı: {response}")
                    return None

    return video_id
