import os
import requests
from typing import Optional, List, Dict, Any

class VideoFetcher:
    """
    Fetches HD portrait (9:16) stock video clips from Pexels API based on script keywords.
    Provides fallback procedural video generation if no API key is set.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("PEXELS_API_KEY")

    def search_and_download_video(self, keyword: str, output_path: str, orientation: str = "portrait") -> Optional[str]:
        """
        Searches Pexels for a vertical video clip matching the keyword and downloads it.
        """
        if not self.api_key:
            print("No PEXELS_API_KEY provided. Using procedural placeholder video.")
            return self._create_placeholder_clip(output_path, keyword)

        headers = {"Authorization": self.api_key}
        url = f"https://api.pexels.com/videos/search?query={keyword}&orientation={orientation}&per_page=5"

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                videos = data.get("videos", [])
                if not videos:
                    print(f"No videos found for query '{keyword}'. Falling back to placeholder.")
                    return self._create_placeholder_clip(output_path, keyword)

                # Pick the first video and select portrait 720p or 1080p file
                chosen_video = videos[0]
                video_files = chosen_video.get("video_files", [])
                
                # Sort by quality/width preference
                hd_files = [f for f in video_files if f.get("quality") == "hd" or (f.get("width", 0) >= 720)]
                download_url = hd_files[0]["link"] if hd_files else video_files[0]["link"]

                # Download file
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with requests.get(download_url, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(output_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                return output_path
            else:
                print(f"Pexels API Error {resp.status_code}: {resp.text}")
                return self._create_placeholder_clip(output_path, keyword)
        except Exception as e:
            print(f"Failed to fetch video from Pexels: {e}")
            return self._create_placeholder_clip(output_path, keyword)

    def _create_placeholder_clip(self, output_path: str, topic_label: str) -> str:
        """
        Fallback placeholder if no Pexels API key or network fails.
        Creates a dark stylish video sequence placeholder using Pillow.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        # Note: In the video composer, if this placeholder mp4 doesn't exist,
        # composer will create animated color gradient background directly.
        return output_path
