"""
AI Brain Module — Advanced Gemini AI Features
Uses Google AI Studio (Gemini 2.5 Flash) for:
1. Auto Trending Topic Suggestions (niche-based)
2. Multi-Variation Script Generator (3 scripts per topic)
3. Weak Hook Rewriter (makes hooks 10x punchier)
4. Weekly Content Calendar Planner
5. Competitor / Viral Content Analyzer
6. Smart SEO Title & Hashtag Optimizer
"""

import json
import os
from typing import Optional, Dict, Any, List

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None


class AIBrain:
    """Advanced AI capabilities powered by Gemini for content domination."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                pass

    def _call_gemini(self, prompt: str, system: str = "", temperature: float = 0.8) -> Optional[str]:
        """Internal helper to call Gemini and return JSON text."""
        if not self.client:
            return None
        try:
            resp = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system or "You are a viral content strategist. Always respond in valid JSON.",
                    response_mime_type="application/json",
                    temperature=temperature,
                ),
            )
            return resp.text
        except Exception as e:
            return json.dumps({"error": str(e)})

    # ═══════════════════════════════════════════════════════════════
    #  1. TRENDING TOPIC SUGGESTIONS
    # ═══════════════════════════════════════════════════════════════
    def suggest_trending_topics(self, niche: str = "Technology", language: str = "Hinglish", count: int = 10) -> List[Dict[str, str]]:
        """
        AI suggests today's most viral-potential topics based on niche.
        Returns list of {topic, reason, estimated_virality}.
        """
        prompt = f"""
You are a viral content researcher for YouTube Shorts and Instagram Reels in India.

Niche: {niche}
Language: {language}
Date context: September 2026

Suggest {count} trending, high-viral-potential topics that a creator should make reels about RIGHT NOW.
For each topic, explain WHY it will go viral and rate its virality potential (1-10).

Focus on:
- Topics people are actively searching for
- Controversial or surprising angles
- "Did you know?" style facts
- Money/career/life hacks that appeal to 18-30 year olds
- AI and technology breakthroughs

Return JSON array:
[
  {{
    "topic": "exact topic title for a reel",
    "hook_idea": "suggested first 2 seconds hook line",
    "reason": "why this will go viral right now",
    "virality_score": 8,
    "best_hashtags": ["#tag1", "#tag2", "#tag3"]
  }}
]
"""
        raw = self._call_gemini(prompt, temperature=0.9)
        if raw:
            try:
                data = json.loads(raw)
                if isinstance(data, list):
                    return data
                return data.get("topics", [data]) if isinstance(data, dict) else []
            except Exception:
                pass
        # Fallback
        return self._fallback_topics(niche)

    # ═══════════════════════════════════════════════════════════════
    #  2. MULTI-VARIATION SCRIPT GENERATOR
    # ═══════════════════════════════════════════════════════════════
    def generate_script_variations(self, topic: str, language: str = "Hinglish", count: int = 3) -> List[Dict[str, Any]]:
        """
        Generates multiple script variations for the same topic.
        Each variation has a different hook style and angle.
        """
        prompt = f"""
Create {count} COMPLETELY DIFFERENT viral reel scripts for the topic: "{topic}"
Language: {language}

Each script must have a DIFFERENT hook style:
- Variation 1: "Shock / Pattern Interrupt" hook (e.g., "STOP! Don't do this...")
- Variation 2: "Curiosity Gap" hook (e.g., "99% people don't know this secret...")
- Variation 3: "Direct Challenge" hook (e.g., "I bet you can't answer this...")

Each script should be 25-40 seconds when spoken.

Return JSON array:
[
  {{
    "variation_name": "Shock Hook",
    "hook": "the exact first sentence",
    "voiceover_script": "full spoken text start to finish",
    "thumbnail_text": "3-5 bold words for thumbnail",
    "estimated_retention_score": 85
  }}
]
"""
        raw = self._call_gemini(prompt, temperature=0.85)
        if raw:
            try:
                data = json.loads(raw)
                return data if isinstance(data, list) else [data]
            except Exception:
                pass
        return [{"variation_name": "Default", "hook": f"Did you know about {topic}?",
                 "voiceover_script": f"Here is everything about {topic}...",
                 "thumbnail_text": topic[:30], "estimated_retention_score": 60}]

    # ═══════════════════════════════════════════════════════════════
    #  3. HOOK REWRITER (Make weak hooks 10x better)
    # ═══════════════════════════════════════════════════════════════
    def rewrite_hook(self, weak_hook: str, topic: str, language: str = "Hinglish") -> Dict[str, Any]:
        """
        Takes a weak/generic hook and rewrites it into 5 powerful alternatives.
        """
        prompt = f"""
The following hook for a YouTube Short / Instagram Reel is WEAK and generic:
Original hook: "{weak_hook}"
Topic: "{topic}"
Language: {language}

Rewrite this into 5 MUCH MORE POWERFUL hooks using these proven techniques:
1. Pattern Interrupt (unexpected statement)
2. Curiosity Gap (incomplete information)
3. Bold Claim (controversial but true)
4. Question (triggers comment reflex)
5. Story Start (micro-story opening)

Each hook must be under 12 words and instantly grab attention in 2 seconds.

Return JSON:
{{
  "original": "{weak_hook}",
  "rewrites": [
    {{"style": "Pattern Interrupt", "hook": "rewritten hook text", "why_better": "explanation"}},
    {{"style": "Curiosity Gap", "hook": "...", "why_better": "..."}},
    {{"style": "Bold Claim", "hook": "...", "why_better": "..."}},
    {{"style": "Question", "hook": "...", "why_better": "..."}},
    {{"style": "Story Start", "hook": "...", "why_better": "..."}}
  ],
  "best_pick": 0
}}
"""
        raw = self._call_gemini(prompt, temperature=0.8)
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                pass
        return {
            "original": weak_hook,
            "rewrites": [
                {"style": "Pattern Interrupt", "hook": f"STOP! {topic} के बारे में ये मत करना!", "why_better": "Creates urgency"},
                {"style": "Curiosity Gap", "hook": f"99% लोग {topic} में ये गलती करते हैं...", "why_better": "Incomplete info"},
                {"style": "Bold Claim", "hook": f"{topic} से ₹1 लाख कमाना आसान है, अगर...", "why_better": "Bold promise"},
            ],
            "best_pick": 0
        }

    # ═══════════════════════════════════════════════════════════════
    #  4. WEEKLY CONTENT CALENDAR
    # ═══════════════════════════════════════════════════════════════
    def generate_content_calendar(self, niche: str = "Technology", days: int = 7, language: str = "Hinglish") -> List[Dict[str, Any]]:
        """
        AI plans an entire week of content — 2 reels per day with topics, hooks, and best posting times.
        """
        prompt = f"""
You are a content strategist planning a week of YouTube Shorts and Instagram Reels.

Niche: {niche}
Language: {language}
Days to plan: {days}
Posts per day: 2

For each day, suggest 2 reel topics with:
- Specific topic title
- Hook idea (first 2 seconds)
- Best posting time (IST)
- Why this day/time is ideal

Mix content types: educational, shocking facts, how-to, listicle, trend commentary.

Return JSON array:
[
  {{
    "day": "Day 1 (Monday)",
    "posts": [
      {{
        "topic": "topic title",
        "hook": "hook text",
        "post_time": "12:30 PM IST",
        "content_type": "Listicle",
        "reason": "why this timing"
      }},
      {{
        "topic": "...",
        "hook": "...",
        "post_time": "7:00 PM IST",
        "content_type": "Shocking Fact",
        "reason": "..."
      }}
    ]
  }}
]
"""
        raw = self._call_gemini(prompt, temperature=0.85)
        if raw:
            try:
                data = json.loads(raw)
                return data if isinstance(data, list) else [data]
            except Exception:
                pass
        return self._fallback_calendar(niche, days)

    # ═══════════════════════════════════════════════════════════════
    #  5. SCRIPT IMPROVER (Polish existing script)
    # ═══════════════════════════════════════════════════════════════
    def improve_script(self, original_script: str, topic: str, language: str = "Hinglish") -> Dict[str, Any]:
        """
        Takes an existing script and improves it for maximum retention.
        """
        prompt = f"""
You are a world-class viral video script editor.

Original script for topic "{topic}":
---
{original_script}
---

Improve this script for MAXIMUM viewer retention on YouTube Shorts / Instagram Reels:
1. Make the hook more punchy (first sentence)
2. Remove any filler words or slow parts
3. Add a "loop trigger" at the end (connect end to beginning)
4. Make it faster-paced (every sentence should add value)
5. Add a comment-triggering question
6. Keep language: {language}

Return JSON:
{{
  "improved_script": "the full improved voiceover text",
  "changes_made": ["list of specific changes"],
  "retention_boost_estimate": "+15%",
  "loop_trigger": "the specific loop sentence added"
}}
"""
        raw = self._call_gemini(prompt, temperature=0.7)
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                pass
        return {
            "improved_script": original_script,
            "changes_made": ["Could not connect to AI. Script returned as-is."],
            "retention_boost_estimate": "+0%",
        }

    # ═══════════════════════════════════════════════════════════════
    #  6. SEO OPTIMIZER (Title + Description + Hashtags)
    # ═══════════════════════════════════════════════════════════════
    def optimize_seo(self, topic: str, script: str, platform: str = "YouTube Shorts") -> Dict[str, Any]:
        """
        Generates SEO-optimized titles, descriptions, and hashtags.
        """
        prompt = f"""
Generate SEO-optimized metadata for a {platform} video.

Topic: "{topic}"
Script preview: "{script[:200]}"

Provide:
- 5 viral title options (max 60 chars each, with emoji)
- 1 SEO description (100-150 words, keyword-rich)
- 15 trending hashtags (mix of broad and niche)
- 5 search keywords people would use to find this video

Return JSON:
{{
  "titles": ["title1", "title2", "title3", "title4", "title5"],
  "description": "full description text",
  "hashtags": ["#tag1", "#tag2", ...],
  "search_keywords": ["keyword1", "keyword2", ...]
}}
"""
        raw = self._call_gemini(prompt, temperature=0.7)
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                pass
        return {
            "titles": [f"{topic} 🔥", f"Secret of {topic} 🤫"],
            "description": f"Everything about {topic}",
            "hashtags": ["#shorts", "#reels", "#viral", "#trending"],
            "search_keywords": [topic]
        }

    # ─── Fallbacks ────────────────────────────────────────────────
    @staticmethod
    def _fallback_topics(niche: str) -> List[Dict[str, str]]:
        topics_map = {
            "Technology": [
                {"topic": "3 Free AI Tools That Replace Paid Software", "hook_idea": "Stop paying for software!", "reason": "AI tools trending", "virality_score": 9, "best_hashtags": ["#ai", "#free", "#tech"]},
                {"topic": "Python Trick That 99% Developers Don't Know", "hook_idea": "Even senior devs miss this...", "reason": "Coding curiosity", "virality_score": 8, "best_hashtags": ["#python", "#coding", "#dev"]},
                {"topic": "This AI Can Clone Your Voice in 10 Seconds", "hook_idea": "I cloned my voice and...", "reason": "Shock factor", "virality_score": 9, "best_hashtags": ["#ai", "#voice", "#tech"]},
            ],
            "Money / Career": [
                {"topic": "12th Pass Students: 3 Ways to Earn ₹50K/Month", "hook_idea": "College degree is NOT required!", "reason": "Youth audience", "virality_score": 9, "best_hashtags": ["#money", "#career", "#earning"]},
                {"topic": "This Side Hustle Pays ₹2000/Day From Phone", "hook_idea": "I made ₹2000 today just from my phone", "reason": "Money motivation", "virality_score": 8, "best_hashtags": ["#sidehustle", "#income", "#money"]},
            ],
        }
        return topics_map.get(niche, topics_map["Technology"])

    @staticmethod
    def _fallback_calendar(niche: str, days: int) -> List[Dict[str, Any]]:
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        calendar = []
        for i in range(min(days, 7)):
            calendar.append({
                "day": f"Day {i+1} ({day_names[i]})",
                "posts": [
                    {"topic": f"{niche} Tip #{i*2+1}", "hook": "Did you know?", "post_time": "12:30 PM IST", "content_type": "Educational", "reason": "Lunch break traffic"},
                    {"topic": f"{niche} Fact #{i*2+2}", "hook": "Stop scrolling!", "post_time": "7:00 PM IST", "content_type": "Shocking Fact", "reason": "Evening peak"},
                ]
            })
        return calendar

    # ─── Multimodal Vision & Reference Reel Analysis ───────────────
    def analyze_product_photo(self, image_bytes: bytes, product_notes: str = "") -> Dict[str, Any]:
        """
        Analyzes uploaded product photo and generates an Affiliate Reel concept, script, scene breakdown, and editing instructions.
        """
        prompt = f"""
        You are an E-Commerce Video Specialist & Viral Content Strategist.
        Analyze the provided product image and additional notes: "{product_notes}".
        
        Do NOT invent fake specs, claims, or prices without basis. Base your analysis on visual features seen in the image.
        
        Return a strict JSON object with:
        {{
            "detected_product_category": "e.g. Wireless Audio / Fashion / Gadget",
            "key_visual_features": ["feature 1", "feature 2"],
            "target_audience": "e.g. Students, Tech Enthusiasts",
            "reel_concept": "High-converting 9:16 short reel idea",
            "viral_hook": "First 3-second pattern interruption line",
            "voiceover_script": "30-45 second script highlighting real value and call to action",
            "scene_breakdown": [
                {{"time": "0-3s", "visual": "Product image closeup with text overlay", "audio": "Hook line"}},
                {{"time": "3-15s", "visual": "Key features demo", "audio": "Value proposition"}},
                {{"time": "15-30s", "visual": "Call to action with bio link text", "audio": "CTA"}}
            ],
            "editing_instructions": "Pacing, transition style, font colors, and music vibe",
            "caption_and_hashtags": "Post caption with #ad #affiliate disclosure"
        }}
        """
        if not self.client:
            return self._fallback_product_analysis(product_notes)

        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(image_bytes))
            resp = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[img, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(resp.text)
        except Exception as e:
            print(f"[AIBrain Product Image Analysis Error]: {e}")
            return self._fallback_product_analysis(product_notes)

    def analyze_reference_reel_and_product(self, reference_text_or_style: str, image_bytes: Optional[bytes], product_name: str) -> Dict[str, Any]:
        """
        Analyzes a reference reel's style, structure, timing, and presentation, and generates a NEW inspired Affiliate Reel for the user's product.
        Does NOT copy the reference reel directly; creates original content inspired by its structure.
        """
        prompt = f"""
        You are a Viral Content Strategist specializing in Short-Form Video Deconstruction.
        
        Reference Reel Style / Structure: "{reference_text_or_style}"
        Target Product Name: "{product_name}"
        
        Deconstruct the reference reel's viral elements (hook style, pacing, transitions, CTA) and create a NEW, ORIGINAL Affiliate Reel inspired by this style for the target product.
        Do NOT copy the original script word for word.
        
        Return a strict JSON object with:
        {{
            "reference_style_analysis": "Summary of pacing, hook type, and presentation style from reference",
            "inspired_reel_title": "Catchy title",
            "viral_hook": "Opening hook line inspired by reference structure",
            "voiceover_script": "Original script for target product",
            "visual_transitions": ["Transition 1", "Transition 2"],
            "scene_breakdown": [
                {{"scene": 1, "duration": "3s", "description": "Opening hook"}},
                {{"scene": 2, "duration": "12s", "description": "Product feature demo"}},
                {{"scene": 3, "duration": "15s", "description": "Call to action"}}
            ],
            "editing_guidelines": "Cut timing, text placement, and sound effect cues"
        }}
        """
        contents = [prompt]
        if image_bytes:
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(image_bytes))
                contents.insert(0, img)
            except Exception:
                pass

        if not self.client:
            return self._fallback_reference_analysis(product_name)

        try:
            resp = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(resp.text)
        except Exception as e:
            print(f"[AIBrain Reference Reel Analysis Error]: {e}")
            return self._fallback_reference_analysis(product_name)

    @staticmethod
    def _fallback_product_analysis(notes: str) -> Dict[str, Any]:
        return {
            "detected_product_category": "E-Commerce Product / Tech Gadget",
            "key_visual_features": ["High quality build", "Sleek compact design"],
            "target_audience": "Students & Young Professionals",
            "reel_concept": "Unboxing & First Impression Deal Video",
            "viral_hook": "Stop scrolling! Don't buy this product until you watch this!",
            "voiceover_script": f"Here is why everyone is talking about this product. Deal price is super affordable! Check the link in bio to get yours before stock runs out. #ad #affiliate",
            "scene_breakdown": [
                {"time": "0-3s", "visual": "Product photo with bold hook text overlay", "audio": "Stop scrolling!"},
                {"time": "3-15s", "visual": "Product features highlight", "audio": "Key benefits and discount price"},
                {"time": "15-30s", "visual": "Bio link callout", "audio": "Check bio link now!"}
            ],
            "editing_instructions": "Fast cuts, bold yellow text captions, energetic upbeat audio background.",
            "caption_and_hashtags": f"Best deals for you! {notes} #ad #affiliate #AmazonFinds #Deals"
        }

    @staticmethod
    def _fallback_reference_analysis(product_name: str) -> Dict[str, Any]:
        return {
            "reference_style_analysis": "Fast-paced text overlays with pattern-interrupt opening hook and clear CTA.",
            "inspired_reel_title": f"Why Everyone Wants This {product_name}",
            "viral_hook": f"3 Reasons why this {product_name} is going viral!",
            "voiceover_script": f"If you've been looking for the perfect {product_name}, here is what you need to know. It saves time, looks amazing, and costs way less than brand alternatives! Tap link in bio. #ad #affiliate",
            "visual_transitions": ["Zoom in on hook", "Slide left feature list", "Fade out CTA"],
            "scene_breakdown": [
                {"scene": 1, "duration": "3s", "description": "Opening hook with bold text"},
                {"scene": 2, "duration": "12s", "description": "3 Key value points"},
                {"scene": 3, "duration": "15s", "description": "Call to action with bio link"}
            ],
            "editing_guidelines": "Sync cuts with music beat. Keep text centered."
        }
