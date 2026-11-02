"""
Omni-Studio Self-Thinking Algorithm Brain Module for AutoViral AI.
Provides SQLite memory persistence, virality score prediction, and multi-format decision engine.
"""

import os
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "autoviral_omni.db"

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def init_omni_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS algo_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            niche TEXT NOT NULL,
            hook_style TEXT NOT NULL,
            retention_rate REAL DEFAULT 0.0,
            views_count INTEGER DEFAULT 0,
            viral_score REAL DEFAULT 0.0,
            learned_insights TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            format_type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            script TEXT NOT NULL,
            hashtags TEXT,
            status TEXT DEFAULT 'ready',
            video_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_omni_db()

class OmniAlgorithmBrain:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if (GEMINI_AVAILABLE and self.api_key) else None

    def analyze_and_optimize(self, topic: str, niche: str = "Technology & AI") -> dict:
        past_insights = self._get_learned_insights(niche)
        
        prompt = f"""
        You are an Autonomous Social Media Algorithm Expert for AutoViral AI.
        Topic: "{topic}"
        Niche: "{niche}"
        Past Algorithm Learnings: {json.dumps(past_insights)}
        
        Analyze this topic for YouTube Shorts (9:16), Instagram Reels, and YouTube Long Video (16:9).
        Return a strict JSON object with:
        {{
            "recommended_format": "shorts_9_16" or "long_16_9",
            "virality_score_prediction": float (0-100),
            "viral_hook": "High-retention opening line (first 3 seconds)",
            "title": "SEO & Click-optimized title with emojis",
            "description": "Engaging description with key call to action",
            "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
            "script_body": "30 to 45 second fast-paced narration script",
            "background_keywords": ["keyword1", "keyword2"],
            "algo_strategy_reason": "Explanation of why this script/hook will trigger algorithmic push"
        }}
        """
        
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                result = json.loads(response.text)
                self._record_decision(niche, result.get("viral_hook", ""), result.get("virality_score_prediction", 85.0))
                return result
            except Exception as e:
                print(f"[OmniBrain Error]: {e}, using local rule engine.")
        
        return self._local_fallback_brain(topic, niche)

    def _local_fallback_brain(self, topic: str, niche: str) -> dict:
        return {
            "recommended_format": "shorts_9_16",
            "virality_score_prediction": 88.5,
            "viral_hook": f"Stop scrolling! This {topic} secret will change everything.",
            "title": f"⚡ {topic}: Don't Miss This! #Shorts",
            "description": f"Learn everything about {topic} in under 45 seconds! Subscribe for daily AI & tech updates.",
            "hashtags": ["#Shorts", "#AI", "#Tech", "#Tips", "#Viral"],
            "script_body": f"Did you know about {topic}? Most people get this completely wrong. Here is how it actually works step by step. Try this today and see the results for yourself!",
            "background_keywords": ["technology", "cyberpunk", "futuristic"],
            "algo_strategy_reason": "Pattern interruption hook in first 3 seconds maximizes 85%+ retention rate on Reels & Shorts algorithms."
        }

    def _get_learned_insights(self, niche: str) -> list:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT hook_style, viral_score, learned_insights FROM algo_memory WHERE niche=? ORDER BY viral_score DESC LIMIT 5", (niche,))
        rows = cursor.fetchall()
        conn.close()
        return [{"hook": r[0], "score": r[1], "insight": r[2]} for r in rows]

    def _record_decision(self, niche: str, hook: str, score: float):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO algo_memory (platform, niche, hook_style, viral_score, learned_insights) VALUES (?, ?, ?, ?, ?)",
            ("Multi-Platform", niche, hook, score, "High initial curiosity trigger detected.")
        )
        conn.commit()
        conn.close()

if __name__ == "__main__":
    brain = OmniAlgorithmBrain()
    res = brain.analyze_and_optimize("AI Tools for Students 2026")
    print("Omni Brain Output:\n", json.dumps(res, indent=2))
