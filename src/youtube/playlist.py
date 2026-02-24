from utils.logger import logger

def get_or_create_playlist(youtube, playlist_title):
    """
    Finds a playlist by title or creates a new one if it doesn't exist.
    """
    playlist_id = find_playlist(youtube, playlist_title)
    
    if not playlist_id:
        logger.info(f"Oynatma listesi bulunamadı: '{playlist_title}'. Yeni oluşturuluyor...")
        playlist_id = create_playlist(youtube, playlist_title)
    
    return playlist_id

def find_playlist(youtube, title):
    """
    Searches for a playlist by title in the user's account.
    """
    try:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50
        )
        
        while request:
            response = request.execute()
            
            for item in response.get("items", []):
                if item["snippet"]["title"] == title:
                    logger.debug(f"Mevcut oynatma listesi bulundu: '{title}' (ID: {item['id']})")
                    return item["id"]
            
            request = youtube.playlists().list_next(request, response)
            
        return None
    except Exception as e:
        logger.error(f"Oynatma listesi aranırken hata: {str(e)}")
        return None

def create_playlist(youtube, title):
    """
    Creates a new private playlist with the given title.
    """
    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": "Auto-Youtube-Video-Commiter tarafından otomatik oluşturuldu.",
                    "defaultLanguage": "tr"
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        logger.success(f"Yeni oynatma listesi oluşturuldu: '{title}' (ID: {response['id']})")
        return response["id"]
    except Exception as e:
        logger.error(f"Oynatma listesi oluşturulurken hata: {str(e)}")
        return None

def add_video_to_playlist(youtube, video_id, playlist_id):
    """
    Adds a video to the specified playlist.
    """
    try:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
        logger.success("Video oynatma listesine eklendi.")
        return True
    except Exception as e:
        logger.error(f"Video oynatma listesine eklenirken hata: {str(e)}")
        return False
