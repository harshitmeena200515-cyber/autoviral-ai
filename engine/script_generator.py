import json
import os
import re
from typing import Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

class ScriptGenerator:
    """
    Generates viral video scripts, hooks, and metadata optimized for
    YouTube Shorts and Instagram Reels algorithms using Gemini API.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini Client: {e}")

    def generate(self, topic: str, video_type: str = "Short (9:16)", language: str = "Hinglish") -> Dict[str, Any]:
        """
        Generates structured viral script with algorithm triggers.
        """
        if not self.client:
            return self._fallback_template(topic, language)

        system_instruction = (
            "You are a world-class YouTube Shorts and Instagram Reels viral scriptwriter and algorithm strategist. "
            "Your scripts maximize Average View Duration (AVD) and Audience Retention. "
            "Structure: "
            "1. 0-3s Hook: Extreme curiosity gap or pattern interrupt. "
            "2. Body: Fast-paced, concise, punchy facts or tips without intro/filler words. "
            "3. Loop CTA: Connect the end back to the beginning or ask an engaging question for comments. "
            "Always return strictly valid JSON."
        )

        prompt = f"""
Create a viral video script and algorithm metadata for the topic: "{topic}".
Format: {video_type}
Language of voiceover: {language} (use natural conversational spoken tone).

Provide the output ONLY as a valid JSON object matching this schema:
{{
  "title_suggestions": ["Title 1 with high CTR hook", "Title 2 (curiosity gap)", "Title 3 (benefit-driven)"],
  "hook": "The exact first 1-2 punchy sentences to hook the viewer in 0-3 seconds",
  "voiceover_script": "The full spoken voiceover text from start to finish. Make it flow smoothly without stage directions or bracketed text.",
  "scene_cues": [
    {{"timestamp": "0-3s", "visual_prompt": "Fast search query for stock clip", "spoken_text": "text spoken here"}},
    {{"timestamp": "3-15s", "visual_prompt": "Fast search query for stock clip", "spoken_text": "text spoken here"}},
    {{"timestamp": "15-30s", "visual_prompt": "Fast search query for stock clip", "spoken_text": "text spoken here"}}
  ],
  "visual_search_keywords": ["keyword1", "keyword2", "keyword3"],
  "thumbnail_text": "3-5 high impact words for thumbnail overlay",
  "description": "Engaging description for YouTube / Instagram with keywords",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
}}
"""
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.7,
                ),
            )
            data = json.loads(response.text)
            return data
        except Exception as e:
            print(f"Error calling Gemini API: {e}, falling back to intelligent template.")
            return self._fallback_template(topic, language, error_msg=str(e))

    def _fallback_template(self, topic: str, language: str = "Hinglish", error_msg: Optional[str] = None) -> Dict[str, Any]:
        """Provides an intelligent mock template if API key is not yet set."""
        if "hindi" in language.lower():
            script = f"क्या आपको पता है {topic} के बारे में ये सीक्रेट? ज़्यादातर लोग इसमें सबसे बड़ी गलती करते हैं। अगर आप इसे सही तरीक़े से करेंगे तो आपका रिज़ल्ट 10 गुना बेहतर हो सकता है। इसे अभी सेव कर लो ताकि भूल न जाओ!"
            hook = f"क्या आपको पता है {topic} के बारे में ये सीक्रेट?"
            thumb = f"{topic} का सबसे बड़ा सच!"
        else:
            script = f"Stop scrolling if you want to master {topic}! Most people get this completely wrong. Here is the exact strategy that actually works in 2026. Save this reel before you forget!"
            hook = f"Stop scrolling if you want to master {topic}!"
            thumb = f"Secret of {topic}!"

        return {
            "title_suggestions": [
                f"Secret of {topic} Revealed! 🤫",
                f"Don't Make This Mistake in {topic} ⚠️",
                f"How to Master {topic} in 60 Seconds 🚀"
            ],
            "hook": hook,
            "voiceover_script": script,
            "scene_cues": [
                {"timestamp": "0-3s", "visual_prompt": "person surprised looking at smartphone", "spoken_text": hook},
                {"timestamp": "3-15s", "visual_prompt": "focused person typing code laptop technology", "spoken_text": "Body content..."},
                {"timestamp": "15-30s", "visual_prompt": "success growth chart animated", "spoken_text": "Call to action..."}
            ],
            "visual_search_keywords": ["technology", "coding", "focus", "success"],
            "thumbnail_text": thumb,
            "description": f"Everything you need to know about {topic}! Like & Follow for more daily tech and coding secrets. 🚀\n\n#coding #tech #learning",
            "hashtags": ["#shorts", "#reels", "#coding", "#viral", "#tech", "#learnin60seconds"],
            "api_warning": error_msg or "Running in offline/demo mode. Provide GEMINI_API_KEY for custom AI scripts."
        }
