import os
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple

class ThumbnailEngine:
    """
    Creates high-contrast, clickable thumbnails with bold text overlays,
    gradient backgrounds, and badges optimized for CTR.
    """

    @staticmethod
    def create_thumbnail(
        title_text: str,
        output_path: str,
        format_type: str = "Shorts (9:16)",
        badge_text: str = "MUST WATCH 🔥"
    ) -> str:
        """
        Generates thumbnail image with text wrapping and shadow effects.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if "16:9" in format_type or "Long" in format_type:
            width, height = 1280, 720
        else:
            width, height = 1080, 1920

        # 1. Create stylish gradient canvas (Deep navy blue to vibrant purple/dark)
        base_img = Image.new("RGB", (width, height), color=(15, 15, 26))
        draw = ImageDraw.Draw(base_img)

        # Draw vertical gradient
        for y in range(height):
            ratio = y / height
            r = int(18 * (1 - ratio) + 40 * ratio)
            g = int(18 * (1 - ratio) + 10 * ratio)
            b = int(35 * (1 - ratio) + 70 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Add modern framing borders / accent glow
        draw.rectangle([20, 20, width - 20, height - 20], outline=(255, 215, 0), width=6)

        # 3. Add Top Badge (e.g. "NEW 2026", "SECRET")
        badge_box_w = 400
        badge_box_h = 70
        badge_x = (width - badge_box_w) // 2
        badge_y = 120 if height > 1000 else 50
        draw.rounded_rectangle(
            [badge_x, badge_y, badge_x + badge_box_w, badge_y + badge_box_h],
            radius=15,
            fill=(255, 69, 0) # Bold reddish orange
        )
        
        # Fonts
        font_large = ImageFont.load_default()
        
        # Try finding system fonts on Windows
        try:
            win_font = "C:\\Windows\\Fonts\\arialbd.ttf"
            if os.path.exists(win_font):
                font_title = ImageFont.truetype(win_font, size=72 if height > 1000 else 54)
                font_badge = ImageFont.truetype(win_font, size=36 if height > 1000 else 28)
            else:
                font_title = font_large
                font_badge = font_large
        except Exception:
            font_title = font_large
            font_badge = font_large

        # Draw Badge Text
        draw.text((width // 2, badge_y + (badge_box_h // 2)), badge_text, fill=(255, 255, 255), font=font_badge, anchor="mm")

        # 4. Wrap and Draw Main Title with High Contrast & Shadow
        words = title_text.split()
        lines = []
        current_line = []
        chars_per_line = 16 if height > 1000 else 24

        for word in words:
            if sum(len(w) for w in current_line) + len(word) + len(current_line) <= chars_per_line:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        # Center vertically
        total_text_height = len(lines) * (90 if height > 1000 else 70)
        start_y = (height - total_text_height) // 2

        for i, line in enumerate(lines):
            line_y = start_y + i * (90 if height > 1000 else 70)
            text_color = (255, 255, 0) if i % 2 == 0 else (255, 255, 255) # Alternate Yellow and White
            
            # Shadow
            draw.text((width // 2 + 4, line_y + 4), line, fill=(0, 0, 0), font=font_title, anchor="mm")
            # Main Text
            draw.text((width // 2, line_y), line, fill=text_color, font=font_title, anchor="mm")

        # Save image
        base_img.save(output_path, quality=95)
        return output_path
