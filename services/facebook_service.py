from config import FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN
import requests

def upload_video_to_facebook(video_path, caption="Daily Quiz 🎯"):

    if not FACEBOOK_ACCESS_TOKEN:
        raise ValueError("❌ FACEBOOK_ACCESS_TOKEN missing")
    

    url = f"https://graph-video.facebook.com/v19.0/{FACEBOOK_PAGE_ID}/videos"

    files = {
        "source": open(video_path, "rb")
    }

    data = {
        
     
        "description": caption,
        "published": "true",
        "access_token": FACEBOOK_ACCESS_TOKEN,
    }

    response = requests.post(url, files=files, data=data)

    try:
        result = response.json()
        print("📤 Facebook Upload Response:", result)
        return result
    except Exception:
        print("❌ Upload failed:", response.text)
        return None
