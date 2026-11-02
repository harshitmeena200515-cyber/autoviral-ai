"""
Daily Auto-Pilot Scheduler Module
Automates the full daily lifecycle:
1. Picks trending viral topic from AI Brain based on selected niche
2. Generates script, voiceover, thumbnail, and background video
3. Renders final vertical 9:16 Short/Reel
4. Uploads to YouTube Shorts & Instagram Reels automatically
5. Logs execution history and status
"""

import os
import sys
import json
import time
import datetime
from typing import Dict, Any, Optional

from engine.ai_brain import AIBrain
from engine.script_generator import ScriptGenerator
from engine.audio_engine import AudioEngine
from engine.thumbnail_engine import ThumbnailEngine
from engine.video_fetcher import VideoFetcher
from engine.video_composer import VideoComposer
from engine.upload_manager import UploadManager

CONFIG_FILE = "autopilot_config.json"
HISTORY_FILE = "autopilot_history.json"


class DailyScheduler:
    """Manages 100% automated daily video generation & posting."""

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Loads scheduler configuration."""
        default_config = {
            "enabled": False,
            "niche": "Technology",
            "language": "Hinglish",
            "post_times": ["12:30", "19:00"],  # Daily 12:30 PM & 7:00 PM IST
            "voice": "Hindi Male (Madhur)",
            "speed": "+10%",
            "youtube_upload": True,
            "youtube_privacy": "private",  # private by default for safety
            "instagram_upload": False,
            "max_videos_per_day": 2,
            "last_run": None,
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default_config.update(data)
            except Exception:
                pass
        return default_config

    @staticmethod
    def save_config(config: Dict[str, Any]) -> None:
        """Saves scheduler configuration."""
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    @staticmethod
    def get_history() -> list:
        """Returns log of past automated runs."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    @staticmethod
    def add_history_entry(entry: Dict[str, Any]) -> None:
        """Appends an entry to run history."""
        history = DailyScheduler.get_history()
        history.insert(0, entry)  # Newest first
        history = history[:50]  # Keep last 50
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    @classmethod
    def execute_autopilot_cycle(
        cls,
        niche: str = "Technology",
        language: str = "Hinglish",
        voice: str = "Hindi Male (Madhur)",
        speed: str = "+10%",
        youtube_privacy: str = "private",
        gemini_key: Optional[str] = None,
        pexels_key: Optional[str] = None,
        ig_token: Optional[str] = None,
        ig_user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Runs ONE complete auto-pilot cycle:
        AI Topic -> Script -> Voiceover -> Thumbnail -> Video -> Upload
        """
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": start_time,
            "status": "RUNNING",
            "topic": "",
            "video_path": "",
            "youtube_status": "Skipped",
            "youtube_url": "",
            "instagram_status": "Skipped",
            "error": None
        }

        try:
            # 1. Pick Trending Topic
            ai_brain = AIBrain(api_key=gemini_key)
            topics = ai_brain.suggest_trending_topics(niche=niche, language=language, count=5)
            selected = topics[0] if topics else {
                "topic": f"3 Amazing Facts About {niche}",
                "hook_idea": "Wait! Stop scrolling!",
                "best_hashtags": ["#shorts", "#reels", "#viral"]
            }
            topic_title = selected.get("topic", f"{niche} Daily Short")
            log_entry["topic"] = topic_title

            # 2. Generate Viral Script
            gen = ScriptGenerator(api_key=gemini_key)
            script_data = gen.generate(topic_title, "Shorts / Reels (9:16)", language)
            voiceover_text = script_data.get("voiceover_script", "")
            hook = script_data.get("hook", selected.get("hook_idea", ""))
            thumb_text = script_data.get("thumbnail_text", topic_title[:30])
            hashtags = script_data.get("hashtags", selected.get("best_hashtags", ["#shorts"]))

            # 3. Create Output Paths
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            timestamp_suffix = int(time.time())
            audio_path = os.path.join(output_dir, f"auto_audio_{timestamp_suffix}.mp3")
            thumb_path = os.path.join(output_dir, f"auto_thumb_{timestamp_suffix}.jpg")
            bg_path = os.path.join(output_dir, f"auto_bg_{timestamp_suffix}.mp4")
            final_video = os.path.join(output_dir, f"auto_video_{timestamp_suffix}.mp4")

            # 4. Generate Voiceover
            audio_eng = AudioEngine()
            audio_eng.generate_speech(voiceover_text, audio_path, voice_name=voice, rate=speed)

            # 5. Thumbnail & Background
            ThumbnailEngine.create_thumbnail(thumb_text, thumb_path, format_type="Shorts / Reels (9:16)")
            kw = script_data.get("visual_search_keywords", [niche])[0]
            VideoFetcher(api_key=pexels_key).search_and_download_video(kw, bg_path)

            # 6. Compose Video with Subtitles
            VideoComposer().compose_video(
                audio_path=audio_path,
                bg_path=bg_path,
                output_path=final_video,
                script_text=voiceover_text,
                aspect="portrait"
            )
            log_entry["video_path"] = final_video

            # 7. Auto Upload to YouTube
            if os.path.exists("yt_token.json"):
                yt_res = UploadManager.upload_to_youtube(
                    token_path="yt_token.json",
                    video_file_path=final_video,
                    title=f"{topic_title} #Shorts",
                    description=f"{script_data.get('description', '')}\n\n{' '.join(hashtags)}",
                    tags=hashtags,
                    privacy=youtube_privacy
                )
                if yt_res.get("success"):
                    log_entry["youtube_status"] = f"Success ({youtube_privacy})"
                    log_entry["youtube_url"] = yt_res.get("url", "")
                else:
                    log_entry["youtube_status"] = f"Failed: {yt_res.get('error')}"
            else:
                log_entry["youtube_status"] = "Skipped (YouTube not connected)"

            log_entry["status"] = "SUCCESS"
            cls.add_history_entry(log_entry)
            return log_entry

        except Exception as e:
            log_entry["status"] = "FAILED"
            log_entry["error"] = str(e)
            cls.add_history_entry(log_entry)
            return log_entry
