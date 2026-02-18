import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from utils.config import config
from utils.logger import logger

# YouTube API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

def get_youtube_service():
    """
    Authenticates the user and returns the YouTube service object.
    Uses local token.json if available, otherwise starts OAuth flow.
    """
    creds = None
    token_file = 'token.pickle'
    client_secret_file = config.CLIENT_SECRET_FILE

    # 1. Load existing credentials from pickle file
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
            logger.debug("Mevcut oturum (token.pickle) yüklendi.")

    # 2. If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Oturum süresi dolmuş, yenileniyor...")
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secret_file):
                logger.error(f"Hata: '{client_secret_file}' dosyası bulunamadı!")
                logger.info("Lütfen Google Cloud Console'dan istemci sırrını indirin.")
                return None
            
            logger.info("Tarayıcı üzerinden giriş yapmanız bekleniyor...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
            logger.success("Oturum bilgileri (token.pickle) kaydedildi.")

    try:
        service = build('youtube', 'v3', credentials=creds)
        logger.success("YouTube servisi başarıyla oluşturuldu.")
        return service
    except Exception as e:
        logger.error(f"YouTube servisi oluşturulurken hata: {str(e)}")
        return None
