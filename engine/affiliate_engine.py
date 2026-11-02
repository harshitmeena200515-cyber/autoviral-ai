"""
Affiliate Product Research Engine for AutoViral AI.
Supports Amazon India, Flipkart, Meesho, Myntra, and JioMart.
Handles product parsing, price formatting, commission tracking, and ASCI compliance disclosures.
"""

import os
import json
import re
from typing import Dict, Any, Optional

class AffiliateEngine:
    """Manages e-commerce affiliate data and conversion-oriented script templates."""

    PLATFORMS = {
        "amazon": {"name": "Amazon India", "commission_avg": "5% - 10%", "disclosure": "#ad #AmazonFinds #CommissionEarned"},
        "flipkart": {"name": "Flipkart", "commission_avg": "4% - 12%", "disclosure": "#ad #FlipkartHaul #CommissionEarned"},
        "meesho": {"name": "Meesho", "commission_avg": "8% - 15%", "disclosure": "#ad #MeeshoFinds #CommissionEarned"},
        "myntra": {"name": "Myntra", "commission_avg": "6% - 10%", "disclosure": "#ad #MyntraFashion #CommissionEarned"},
        "jiomart": {"name": "JioMart", "commission_avg": "3% - 8%", "disclosure": "#ad #JioMartSavings #CommissionEarned"}
    }

    @staticmethod
    def detect_platform(url_or_name: str) -> str:
        text = url_or_name.lower()
        for p_key in AffiliateEngine.PLATFORMS:
            if p_key in text:
                return p_key
        return "amazon" # Default fallback

    @staticmethod
    def format_affiliate_link(original_url: str, tag: str = "autoviral-21") -> str:
        """Formats or appends affiliate tracking IDs to official URLs without inventing fake links."""
        if not original_url or not original_url.startswith("http"):
            return "https://amazon.in/?tag=" + tag
        
        platform = AffiliateEngine.detect_platform(original_url)
        if platform == "amazon":
            if "?" in original_url:
                return f"{original_url}&tag={tag}"
            return f"{original_url}?tag={tag}"
        return original_url

    @staticmethod
    def build_affiliate_metadata(product_title: str, price: str, original_price: str, platform: str, url: str) -> Dict[str, Any]:
        p_info = AffiliateEngine.PLATFORMS.get(platform.lower(), AffiliateEngine.PLATFORMS["amazon"])
        
        # Calculate discount % safely
        discount_text = ""
        try:
            p_val = float(re.sub(r'[^\d.]', '', price))
            op_val = float(re.sub(r'[^\d.]', '', original_price))
            if op_val > p_val:
                discount_pct = int(((op_val - p_val) / op_val) * 100)
                discount_text = f"{discount_pct}% OFF"
        except Exception:
            discount_text = "Special Deal"

        formatted_link = AffiliateEngine.format_affiliate_link(url)
        
        return {
            "platform_name": p_info["name"],
            "product_title": product_title,
            "price": price,
            "original_price": original_price,
            "discount_text": discount_text,
            "est_commission": p_info["commission_avg"],
            "affiliate_link": formatted_link,
            "disclosure": p_info["disclosure"],
            "asci_compliance_note": "Includes mandatory #ad disclosure for compliance with ASCI & FTC guidelines."
        }

    @staticmethod
    def get_conversion_hook_templates(product_name: str, price: str) -> list:
        return [
            f"Stop buying expensive items! Check this {product_name} for just {price}!",
            f"3 Reasons why everyone is obsessed with this {product_name} under {price}!",
            f"Meesho vs Amazon: Is this {product_name} actually worth {price}?",
            f"Don't make this mistake before buying {product_name}! Watch till the end.",
            f"Unboxing the viral {product_name}: Expectation vs Reality!"
        ]

if __name__ == "__main__":
    meta = AffiliateEngine.build_affiliate_metadata(
        "Wireless Noise Cancelling Earbuds", "₹1,299", "₹2,999", "amazon", "https://amazon.in/dp/B08X123"
    )
    print("Affiliate Engine Test Output:\n", json.dumps(meta, indent=2))
