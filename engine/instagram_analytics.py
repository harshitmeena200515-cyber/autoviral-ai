"""
Instagram Analytics Module
Connects to Instagram Business account via Graph API and fetches:
- Account info (followers, media count)
- Recent media performance (likes, comments, plays)
- Insights (reach, impressions)
- Engagement rate calculation
"""

import os
import datetime
import requests
from typing import Optional, Dict, Any, List


class InstagramAnalytics:
    """Fetches Instagram Business account insights via Graph API."""

    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self, access_token: Optional[str] = None, ig_user_id: Optional[str] = None):
        self.access_token = access_token or os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.ig_user_id = ig_user_id or os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")

    def is_connected(self) -> bool:
        return bool(self.access_token and self.ig_user_id)

    # ─── Account Info ─────────────────────────────────────────────
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Returns followers count, media count, username, profile pic."""
        if not self.is_connected():
            return None
        try:
            url = f"{self.BASE_URL}/{self.ig_user_id}"
            params = {
                "fields": "username,name,followers_count,follows_count,media_count,profile_picture_url,biography",
                "access_token": self.access_token
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "username": data.get("username", ""),
                    "name": data.get("name", ""),
                    "followers": data.get("followers_count", 0),
                    "following": data.get("follows_count", 0),
                    "media_count": data.get("media_count", 0),
                    "profile_pic": data.get("profile_picture_url", ""),
                    "bio": data.get("biography", ""),
                }
            return {"error": f"API Error {resp.status_code}: {resp.text[:200]}"}
        except Exception as e:
            return {"error": str(e)}

    # ─── Recent Media Performance ────────────────────────────────
    def get_recent_media(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns recent posts/reels with likes, comments, and plays."""
        if not self.is_connected():
            return []
        try:
            url = f"{self.BASE_URL}/{self.ig_user_id}/media"
            params = {
                "fields": "id,caption,media_type,media_url,thumbnail_url,timestamp,like_count,comments_count,permalink",
                "limit": limit,
                "access_token": self.access_token
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                items = resp.json().get("data", [])
                media_list = []
                for item in items:
                    media_list.append({
                        "id": item.get("id", ""),
                        "caption": (item.get("caption", "") or "")[:80],
                        "media_type": item.get("media_type", ""),
                        "thumbnail": item.get("thumbnail_url") or item.get("media_url", ""),
                        "timestamp": item.get("timestamp", ""),
                        "likes": item.get("like_count", 0),
                        "comments": item.get("comments_count", 0),
                        "permalink": item.get("permalink", ""),
                    })
                return media_list
            return [{"error": f"API Error {resp.status_code}"}]
        except Exception as e:
            return [{"error": str(e)}]

    # ─── Account Insights (Reach, Impressions) ────────────────────
    def get_insights(self, period: str = "day", days: int = 28) -> Optional[Dict[str, Any]]:
        """Fetches account-level insights: reach, impressions, profile views."""
        if not self.is_connected():
            return None
        try:
            url = f"{self.BASE_URL}/{self.ig_user_id}/insights"
            params = {
                "metric": "reach,impressions,profile_views",
                "period": period,
                "access_token": self.access_token
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                result = {}
                for metric in data:
                    name = metric.get("name", "")
                    values = metric.get("values", [])
                    total = sum(v.get("value", 0) for v in values)
                    result[name] = {
                        "total": total,
                        "daily": [{"date": v.get("end_time", ""), "value": v.get("value", 0)} for v in values]
                    }
                return result
            return {"error": f"API Error {resp.status_code}: {resp.text[:200]}"}
        except Exception as e:
            return {"error": str(e)}

    # ─── Engagement Rate ──────────────────────────────────────────
    def calculate_engagement_rate(self, account_info: Dict, recent_media: List) -> float:
        """Calculates engagement rate = (avg likes + comments) / followers × 100."""
        followers = account_info.get("followers", 1)
        if not recent_media or followers == 0:
            return 0.0
        total_engagement = sum(m.get("likes", 0) + m.get("comments", 0) for m in recent_media if "error" not in m)
        avg_engagement = total_engagement / max(len(recent_media), 1)
        return round((avg_engagement / followers) * 100, 2)

    # ─── Demo Data ────────────────────────────────────────────────
    @staticmethod
    def get_demo_data() -> Dict[str, Any]:
        """Realistic demo data for preview."""
        import random
        today = datetime.date.today()
        dates = [(today - datetime.timedelta(days=i)).isoformat() for i in range(27, -1, -1)]
        base_reach = 200
        reach_values = [base_reach + random.randint(-80, 300) + (i * 8) for i, _ in enumerate(dates)]

        return {
            "account": {
                "username": "your_account (Demo)",
                "followers": 1245,
                "following": 340,
                "media_count": 38,
            },
            "recent_media": [
                {"caption": "3 AI Coding Secrets 🤯", "likes": 890, "comments": 67, "media_type": "VIDEO"},
                {"caption": "Money Tips for Students 💰", "likes": 560, "comments": 34, "media_type": "VIDEO"},
                {"caption": "Python Tricks Nobody Knows", "likes": 420, "comments": 23, "media_type": "VIDEO"},
                {"caption": "ChatGPT vs Gemini 2026", "likes": 310, "comments": 15, "media_type": "VIDEO"},
            ],
            "insights": {
                "reach": {"total": sum(reach_values), "daily": [{"date": d, "value": v} for d, v in zip(dates, reach_values)]},
                "impressions": {"total": int(sum(reach_values) * 1.8)},
            },
            "engagement_rate": 4.2
        }
