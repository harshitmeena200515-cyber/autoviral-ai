import os
from typing import Optional, Dict, Any, List

class YouTubePublisher:
    """
    Handles YouTube Data API v3 video uploads, metadata formatting,
    and provides exact step-by-step instructions for monetizing & running ads.
    """

    @staticmethod
    def get_upload_metadata(title: str, description: str, hashtags: List[str], category_id: str = "27") -> Dict[str, Any]:
        """
        Formats metadata strictly complying with YouTube Data API v3 videos.insert schema.
        Category 27 = Education, 28 = Science & Tech.
        """
        # Clean tags (remove leading '#' for YouTube tags list)
        clean_tags = [t.replace("#", "").strip() for t in hashtags if t.strip()]
        
        # Ensure #Shorts is in title/description for Shorts shelf detection
        full_title = f"{title} #Shorts" if "#shorts" not in title.lower() else title
        full_description = f"{description}\n\n" + " ".join(hashtags)

        return {
            "snippet": {
                "title": full_title[:100],
                "description": full_description[:5000],
                "tags": clean_tags[:30],
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "private", # Default to private so user can inspect on YouTube Studio before going public
                "selfDeclaredMadeForKids": False
            }
        }

    @staticmethod
    def get_monetization_and_ad_guide() -> List[Dict[str, str]]:
        """
        Step-by-step guide for turning on Ads and Monetization on YouTube & Instagram.
        """
        return [
            {
                "step": "1. YouTube Partner Program (YPP) Eligibility",
                "detail": "Need 1,000 subscribers + either 10 Million Shorts views in 90 days OR 4,000 public watch hours on long videos."
            },
            {
                "step": "2. Turning on Ads (YouTube Studio)",
                "detail": "Once approved, go to YouTube Studio > Earn > Watch Page Ads / Shorts Feed Ads and click 'Turn on'. Ads run automatically."
            },
            {
                "step": "3. Running Google Ads for Rapid Channel Growth (Optional)",
                "detail": "In Google Ads (ads.google.com), create a 'Video campaign' > 'Drive views/engagement'. Set budget to ₹100-₹200/day to test which hooks get the highest subscriber conversion."
            },
            {
                "step": "4. Brand Deals & Affiliate Links",
                "detail": "Even before 1,000 subs, put affiliate links (Amazon, software tools) in your pinned comments or Instagram bio. Earn ₹500 to ₹5,000 per sale."
            }
        ]
