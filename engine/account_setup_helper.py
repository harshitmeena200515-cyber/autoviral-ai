"""
Branding & Account Asset Generator
Creates algorithm-optimized assets for YouTube & Instagram:
- High-res Avatar / Profile Picture (PNG)
- YouTube Channel Banner (2048x1152 PNG)
- Complete SEO Profile Metadata (Name, Bio, Tags, Keywords, Description)
"""

import os
import json
from PIL import Image, ImageDraw, ImageFont


class AccountAssetGenerator:
    """Generates ready-to-use profile assets and SEO settings."""

    @staticmethod
    def generate_profile_avatar(name_initial: str = "AV", output_path: str = "output/avatar.png") -> str:
        """Generates a modern, sleek gradient avatar for YouTube & Instagram (800x800)."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img = Image.new("RGB", (800, 800), color=(15, 15, 26))
        draw = ImageDraw.Draw(img)

        # Gradient circle
        center = (400, 400)
        radius = 350
        # Draw outer glowing ring
        draw.ellipse([center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
                     fill=(30, 20, 50), outline=(255, 75, 75), width=12)

        # Draw inner circle
        inner_r = 320
        draw.ellipse([center[0] - inner_r, center[1] - inner_r, center[0] + inner_r, center[1] + inner_r],
                     fill=(20, 10, 35))

        # Big letters
        draw.text((400, 380), name_initial, fill=(255, 255, 255), anchor="mm")
        img.save(output_path, "PNG")
        return output_path

    @staticmethod
    def generate_channel_banner(title: str = "AUTOVIRAL AI", subtitle: str = "DAILY AI TOOLS & WEALTH SECRETS", output_path: str = "output/banner.png") -> str:
        """Generates official YouTube banner (2048x1152)."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 2048 x 1152 banner
        img = Image.new("RGB", (2048, 1152), color=(10, 10, 20))
        draw = ImageDraw.Draw(img)

        # Safe area is center 1235x338 (from y=407 to y=745)
        # Draw a stylish dark gradient box in safe area
        draw.rectangle([0, 407, 2048, 745], fill=(18, 18, 35))
        draw.line([0, 407, 2048, 407], fill=(255, 75, 75), width=4)
        draw.line([0, 745, 2048, 745], fill=(0, 200, 83), width=4)

        # Title & Subtitle
        draw.text((1024, 530), title, fill=(255, 255, 255), anchor="mm")
        draw.text((1024, 620), f"⚡ {subtitle} ⚡", fill=(255, 180, 50), anchor="mm")
        draw.text((1024, 680), "NEW SHORTS EVERY DAY @ 12:30 PM & 7:00 PM IST", fill=(170, 170, 190), anchor="mm")

        img.save(output_path, "PNG")
        return output_path

    @staticmethod
    def get_optimized_account_blueprint(niche: str = "Tech & Earning") -> dict:
        """Returns ready-made SEO settings for YouTube & Instagram."""
        return {
            "youtube": {
                "recommended_names": [
                    "TechKaSikandar",
                    "CodeEarnAI",
                    "ViralTechShorts",
                    "HarshitTechAI"
                ],
                "handle_suggestions": ["@TechKaSikandar", "@CodeEarnAI", "@HarshitTechAI"],
                "channel_description": (
                    "🚀 Welcome to your daily dose of AI Tools, Coding Hacks, and Online Career Secrets!\n\n"
                    "💡 Yahan hum 12th pass students aur beginners ko sikhate hain ki AI aur coding ka use karke "
                    "kaise smart work aur earning ki ja sakti hai.\n\n"
                    "⏰ New Shorts Daily at 12:30 PM & 7:00 PM IST.\n"
                    "🔔 Subscribe now to stay ahead of 99% people!"
                ),
                "channel_keywords": [
                    "ai tools", "how to earn money online", "student earning", "coding for beginners",
                    "python tricks", "gemini ai", "youtube shorts hindi", "tech hacks", "make money with ai"
                ],
                "category": "Science & Technology (28) or Education (27)",
                "made_for_kids": "No (Setting this ensures comments & community tab stay active)"
            },
            "instagram": {
                "username_suggestions": ["code.earn.ai", "tech.sikandar", "harshit.ai.hacks"],
                "name_field_seo": "Harshit | AI & Career Hacks 🚀",
                "category": "Digital Creator",
                "bio": (
                    "💡 Daily AI Tools & Career Hacks for Students\n"
                    "🔥 Code, Create & Earn with AI\n"
                    "🚀 0 to ₹50K Blueprint 👇\n"
                    "🔗 youtube.com/@YourChannel"
                ),
                "account_type": "Creator Account (Free insights & trending audio access)"
            }
        }
