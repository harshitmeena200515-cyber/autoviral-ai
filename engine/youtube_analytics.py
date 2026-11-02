"""
YouTube Analytics Module
Connects to user's YouTube channel via OAuth 2.0 and fetches:
- Channel stats (subscribers, total views, video count)
- Recent video performance (views, likes, comments per video)
- 28-day trend data (daily views)
- Revenue data (if monetized)
"""

import os
import json
import datetime
from typing import Optional, Dict, Any, List

# These will be available after pip install
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
except ImportError:
    build = None

# Scopes required: read-only channel data + analytics + upload
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


class YouTubeAnalytics:
    """Fetches real-time YouTube channel and video analytics."""

    def __init__(self, client_secrets_path: Optional[str] = None, token_path: str = "yt_token.json"):
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.credentials = None
        self.youtube = None
        self.yt_analytics = None

    # ─── Authentication ────────────────────────────────────────────
    def authenticate(self, client_secrets_json: Optional[str] = None) -> bool:
        """
        Performs OAuth 2.0 flow. On first run opens browser for consent.
        Subsequent runs use saved token.
        Returns True if authenticated successfully.
        """
        if not build:
            return False

        creds = None

        # 1. Try loading saved token
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception:
                creds = None

        # 2. Refresh or re-authenticate
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds or not creds.valid:
            if self.client_secrets_path and os.path.exists(self.client_secrets_path):
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_path, SCOPES)
                creds = flow.run_local_server(port=8090, open_browser=True)
            elif client_secrets_json:
                # Accept JSON string directly (for Streamlit secrets)
                import tempfile
                with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
                    tmp.write(client_secrets_json)
                    tmp_path = tmp.name
                flow = InstalledAppFlow.from_client_secrets_file(tmp_path, SCOPES)
                creds = flow.run_local_server(port=8090, open_browser=True)
                os.unlink(tmp_path)
            else:
                return False

            # Save token for next time
            with open(self.token_path, "w") as f:
                f.write(creds.to_json())

        self.credentials = creds
        self.youtube = build("youtube", "v3", credentials=creds)
        try:
            self.yt_analytics = build("youtubeAnalytics", "v2", credentials=creds)
        except Exception:
            self.yt_analytics = None
        return True

    # ─── Channel Stats ────────────────────────────────────────────
    def get_channel_stats(self) -> Optional[Dict[str, Any]]:
        """Returns channel name, subscribers, total views, video count."""
        if not self.youtube:
            return None
        try:
            resp = self.youtube.channels().list(
                part="snippet,statistics",
                mine=True
            ).execute()
            items = resp.get("items", [])
            if not items:
                return None
            ch = items[0]
            stats = ch.get("statistics", {})
            snippet = ch.get("snippet", {})
            return {
                "channel_id": ch["id"],
                "channel_name": snippet.get("title", "Unknown"),
                "channel_thumbnail": snippet.get("thumbnails", {}).get("default", {}).get("url", ""),
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0)),
                "hidden_subscriber_count": stats.get("hiddenSubscriberCount", False),
            }
        except Exception as e:
            return {"error": str(e)}

    # ─── Recent Videos Performance ────────────────────────────────
    def get_recent_videos(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Returns list of recent videos with per-video stats."""
        if not self.youtube:
            return []
        try:
            # Step 1: Search for recent uploads
            search_resp = self.youtube.search().list(
                part="snippet",
                forMine=True,
                type="video",
                order="date",
                maxResults=max_results
            ).execute()
            video_ids = [item["id"]["videoId"] for item in search_resp.get("items", [])]
            if not video_ids:
                return []

            # Step 2: Get statistics for each video
            stats_resp = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(video_ids)
            ).execute()

            videos = []
            for item in stats_resp.get("items", []):
                s = item.get("statistics", {})
                sn = item.get("snippet", {})
                videos.append({
                    "video_id": item["id"],
                    "title": sn.get("title", ""),
                    "published_at": sn.get("publishedAt", ""),
                    "thumbnail": sn.get("thumbnails", {}).get("medium", {}).get("url", ""),
                    "views": int(s.get("viewCount", 0)),
                    "likes": int(s.get("likeCount", 0)),
                    "comments": int(s.get("commentCount", 0)),
                    "duration": item.get("contentDetails", {}).get("duration", ""),
                    "url": f"https://youtube.com/watch?v={item['id']}"
                })
            return sorted(videos, key=lambda v: v["views"], reverse=True)
        except Exception as e:
            return [{"error": str(e)}]

    # ─── 28-Day Trend ─────────────────────────────────────────────
    def get_views_trend(self, days: int = 28) -> Optional[Dict[str, Any]]:
        """Returns daily views for the last N days using YouTube Analytics API."""
        if not self.yt_analytics:
            return None
        try:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days)
            resp = self.yt_analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics="views,estimatedMinutesWatched,subscribersGained",
                dimensions="day",
                sort="day"
            ).execute()
            rows = resp.get("rows", [])
            dates = [r[0] for r in rows]
            views = [r[1] for r in rows]
            watch_mins = [r[2] for r in rows]
            subs_gained = [r[3] for r in rows]
            return {
                "dates": dates,
                "views": views,
                "watch_minutes": watch_mins,
                "subscribers_gained": subs_gained
            }
        except Exception as e:
            return {"error": str(e)}

    # ─── Revenue (if monetized) ───────────────────────────────────
    def get_revenue(self, days: int = 28) -> Optional[Dict[str, Any]]:
        """Returns estimated revenue for last N days."""
        if not self.yt_analytics:
            return None
        try:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=days)
            resp = self.yt_analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics="estimatedRevenue,estimatedAdRevenue,grossRevenue",
                dimensions="day",
                sort="day"
            ).execute()
            rows = resp.get("rows", [])
            total_revenue = sum(r[1] for r in rows) if rows else 0
            return {
                "total_estimated_revenue": round(total_revenue, 2),
                "currency": "USD",
                "daily_revenue": [{"date": r[0], "revenue": round(r[1], 2)} for r in rows]
            }
        except Exception as e:
            return {"error": str(e)}

    # ─── Demo/Mock Data ───────────────────────────────────────────
    @staticmethod
    def get_demo_data() -> Dict[str, Any]:
        """Returns realistic demo data for preview when not connected."""
        import random
        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=i)).isoformat() for i in range(27, -1, -1)]
        base_views = 150
        views = [base_views + random.randint(-50, 200) + (i * 5) for i, _ in enumerate(dates)]

        return {
            "channel": {
                "channel_name": "Your Channel (Demo)",
                "subscribers": 347,
                "total_views": sum(views),
                "video_count": 24,
            },
            "recent_videos": [
                {"title": "3 AI Coding Secrets 🤯", "views": 12500, "likes": 340, "comments": 89},
                {"title": "Money Tips for Students 💰", "views": 8200, "likes": 210, "comments": 45},
                {"title": "Python Tricks Nobody Knows", "views": 5100, "likes": 180, "comments": 32},
                {"title": "ChatGPT vs Gemini 2026", "views": 3400, "likes": 95, "comments": 18},
                {"title": "Free Hosting Secrets 🚀", "views": 2100, "likes": 67, "comments": 12},
            ],
            "trend": {
                "dates": dates,
                "views": views,
            }
        }
