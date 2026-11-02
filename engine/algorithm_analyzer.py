import re
from typing import Dict, Any, List

class AlgorithmAnalyzer:
    """
    Analyzes scripts, hooks, and metadata against YouTube Shorts and Instagram Reels
    algorithms to maximize Retention, Viewed vs Swiped Away (VVSA), and engagement.
    """

    def analyze_script(self, script_text: str, hook_text: str, title: str) -> Dict[str, Any]:
        """
        Scores the content for algorithmic virality and provides concrete suggestions.
        """
        word_count = len(script_text.split())
        # Speaking rate is typically ~2.5 words per second in fast-paced reels
        est_duration_seconds = round(word_count / 2.5, 1)

        # 1. Hook Score (0-30 points)
        hook_score = 15
        hook_reasons = []
        hook_lower = hook_text.lower()
        
        curiosity_words = ["secret", "mistake", "stop", "never", "why", "truth", "क्यो", "गलती", "सच", "रहस्य", "सीक्रेट", "मत करना"]
        found_curiosity = [w for w in curiosity_words if w in hook_lower]
        if found_curiosity:
            hook_score += 10
            hook_reasons.append(f"Strong curiosity trigger words detected ({', '.join(found_curiosity)})")
        else:
            hook_reasons.append("Add a curiosity trigger (e.g. 'Stop', 'The biggest mistake', 'Secret')")

        if len(hook_text.split()) <= 12:
            hook_score += 5
            hook_reasons.append("Short & punchy hook (under 12 words)")
        else:
            hook_reasons.append("Hook is too long. Keep under 10-12 words for <3s impact.")

        # 2. Pacing & Length Score (0-30 points)
        pacing_score = 20
        pacing_reasons = []
        if 20 <= est_duration_seconds <= 45:
            pacing_score += 10
            pacing_reasons.append(f"Ideal viral sweet spot: {est_duration_seconds}s (optimal for >85% retention).")
        elif est_duration_seconds < 20:
            pacing_score += 5
            pacing_reasons.append(f"Very short ({est_duration_seconds}s). Good for loop rate, but provide enough value.")
        else:
            pacing_reasons.append(f"Longer duration ({est_duration_seconds}s). Requires high visual pacing every 2 seconds.")

        # 3. Engagement & Loop Trigger Score (0-20 points)
        engagement_score = 10
        eng_reasons = []
        cta_words = ["comment", "save", "share", "follow", "कमेंट", "फॉलो", "शेयर", "सेव", "?", "सोचते"]
        if any(w in script_text.lower() for w in cta_words):
            engagement_score += 10
            eng_reasons.append("Includes clear engagement call-to-action or comment question.")
        else:
            eng_reasons.append("Add a question at the end to boost comments (critical for Instagram ranking).")

        # 4. Title / CTR Score (0-20 points)
        title_score = 10
        title_reasons = []
        if any(c in title for c in ["?", "!", "🔥", "🚀", "⚠️", "🤫"]):
            title_score += 5
            title_reasons.append("Emotional/Attention punctuation or emoji in title.")
        if len(title) <= 60:
            title_score += 5
            title_reasons.append("Title length is optimal for mobile feeds without truncation.")

        total_score = hook_score + pacing_score + engagement_score + title_score

        # Categorize
        if total_score >= 85:
            virality_grade = "🔥 High Viral Potential (A+)"
        elif total_score >= 70:
            virality_grade = "⚡ Good Reach Expected (B+)"
        else:
            virality_grade = "⚠️ Needs Optimization (C)"

        return {
            "total_score": total_score,
            "virality_grade": virality_grade,
            "est_duration_seconds": est_duration_seconds,
            "word_count": word_count,
            "metrics": {
                "hook_score": f"{hook_score}/30",
                "pacing_score": f"{pacing_score}/30",
                "engagement_score": f"{engagement_score}/20",
                "title_score": f"{title_score}/20",
            },
            "recommendations": hook_reasons + pacing_reasons + eng_reasons + title_reasons
        }

    @staticmethod
    def get_platform_algorithm_rules() -> Dict[str, Any]:
        """
        Returns up-to-date algorithmic priorities for YouTube Shorts & Instagram Reels.
        """
        return {
            "youtube_shorts": {
                "top_metric_1": "Viewed vs Swiped Away (VVSA) > 75%",
                "top_metric_2": "Average Percentage Viewed (APV) > 100% (Loops are king)",
                "ranking_cycle": "Initial test on 100-500 viewers in first 2-6 hours. If VVSA > 75%, pushed to larger audience.",
                "best_posting_times_ist": ["12:00 PM - 02:00 PM (Lunch break)", "06:00 PM - 09:00 PM (Evening peak)"],
                "monetization": "YouTube Partner Program (YPP) requires 1,000 subscribers + 10M Shorts views (in 90 days) or 4,000 long-form watch hours."
            },
            "instagram_reels": {
                "top_metric_1": "Sends / Shares (via DM) carries the heaviest viral weight.",
                "top_metric_2": "Saves / Bookmarks (indicates high educational/entertainment value).",
                "ranking_cycle": "Shown to followers first, then 'Explore' and 'Reels tab' within 24-48 hours.",
                "best_posting_times_ist": ["09:00 AM - 11:00 AM", "07:00 PM - 10:00 PM"],
                "monetization": "Brand sponsorships, affiliate marketing links in bio, Instagram Gifts, and broadcast channels."
            },
            "ads_and_monetization_guide": {
                "organic_ads_earnings": "Once eligible for YPP, YouTube puts ads between Shorts in the feed and distributes ad pool revenue based on your share of views.",
                "paid_ads_growth": "You can promote videos via Google Ads (Video Action Campaigns) for ₹0.20 to ₹0.80 per view to rapidly test hooks or build initial subscribers.",
                "sponsorship_rate": "Even with 10k-50k views per reel, niche tech creators charge ₹2,000 to ₹10,000 per brand mention."
            }
        }
