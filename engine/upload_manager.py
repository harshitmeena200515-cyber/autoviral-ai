"""
Upload Manager
Handles uploading generated videos to:
1. YouTube Shorts (via YouTube Data API v3 - resumable upload)
2. Instagram Reels (via Instagram Graph API - 2-step publish)
"""

import os
import time
import requests
from typing import Optional, Dict, Any

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
except ImportError:
    build = None
    MediaFileUpload = None


class UploadManager:
    """Manages video uploads to YouTube and Instagram."""

    # ═══════════════════════════════════════════════════════════════
    #  YOUTUBE UPLOAD
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def upload_to_youtube(
        token_path: str,
        video_file_path: str,
        title: str,
        description: str,
        tags: list,
        category_id: str = "27",
        privacy: str = "private"
    ) -> Dict[str, Any]:
        """
        Uploads an MP4 video to YouTube using saved OAuth token.
        Returns dict with video_id and url on success, or error message.
        """
        if not build or not MediaFileUpload:
            return {"error": "google-api-python-client not installed"}

        if not os.path.exists(token_path):
            return {"error": "YouTube not connected. Please authenticate first in the Dashboard tab."}

        if not os.path.exists(video_file_path):
            return {"error": f"Video file not found: {video_file_path}"}

        try:
            SCOPES = [
                "https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube.readonly",
            ]
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            youtube = build("youtube", "v3", credentials=creds)

            # Ensure #Shorts is in title for Shorts shelf detection
            if "#shorts" not in title.lower():
                title = f"{title} #Shorts"

            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description[:5000],
                    "tags": [t.replace("#", "").strip() for t in tags[:30]],
                    "categoryId": category_id,
                },
                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False,
                }
            }

            media = MediaFileUpload(
                video_file_path,
                mimetype="video/mp4",
                resumable=True,
                chunksize=5 * 1024 * 1024  # 5MB chunks
            )

            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()

            video_id = response.get("id", "")
            return {
                "success": True,
                "video_id": video_id,
                "url": f"https://youtube.com/shorts/{video_id}",
                "studio_url": f"https://studio.youtube.com/video/{video_id}/edit",
                "privacy": privacy,
                "message": f"Video uploaded successfully as {privacy}!"
            }

        except Exception as e:
            return {"error": f"YouTube upload failed: {str(e)}"}

    # ═══════════════════════════════════════════════════════════════
    #  INSTAGRAM REELS UPLOAD
    # ═══════════════════════════════════════════════════════════════
    @staticmethod
    def upload_to_instagram(
        access_token: str,
        ig_user_id: str,
        video_url: str,
        caption: str,
        cover_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Publishes a Reel to Instagram Business account.
        Instagram requires the video to be at a publicly accessible URL.

        Two-step process:
        1. Create media container (POST /{ig-user-id}/media)
        2. Publish container (POST /{ig-user-id}/media_publish)
        """
        BASE = "https://graph.facebook.com/v21.0"

        if not access_token or not ig_user_id:
            return {"error": "Instagram not connected. Add access token and business account ID."}

        try:
            # Step 1: Create media container
            container_params = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption[:2200],
                "access_token": access_token,
            }
            if cover_url:
                container_params["cover_url"] = cover_url

            resp = requests.post(f"{BASE}/{ig_user_id}/media", data=container_params, timeout=30)
            if resp.status_code != 200:
                return {"error": f"Container creation failed: {resp.text[:300]}"}

            creation_id = resp.json().get("id")
            if not creation_id:
                return {"error": "No creation_id returned from Instagram"}

            # Step 2: Wait for server-side processing (poll status)
            for attempt in range(30):  # Max 5 minutes wait
                status_resp = requests.get(
                    f"{BASE}/{creation_id}",
                    params={"fields": "status_code", "access_token": access_token},
                    timeout=10
                )
                if status_resp.status_code == 200:
                    status = status_resp.json().get("status_code", "")
                    if status == "FINISHED":
                        break
                    elif status == "ERROR":
                        return {"error": "Instagram rejected the video. Check format (9:16, ≤90s, MP4)."}
                time.sleep(10)

            # Step 3: Publish
            publish_resp = requests.post(
                f"{BASE}/{ig_user_id}/media_publish",
                data={"creation_id": creation_id, "access_token": access_token},
                timeout=30
            )
            if publish_resp.status_code == 200:
                media_id = publish_resp.json().get("id", "")
                return {
                    "success": True,
                    "media_id": media_id,
                    "message": "Reel published to Instagram successfully!",
                    "url": f"https://www.instagram.com/reel/{media_id}/"
                }
            else:
                return {"error": f"Publish failed: {publish_resp.text[:300]}"}

        except Exception as e:
            return {"error": f"Instagram upload failed: {str(e)}"}
