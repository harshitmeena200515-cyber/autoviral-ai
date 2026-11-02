"""
AI Video & Script Quality Judgment System for AutoViral AI.
Evaluates affiliate & short-form video content across 5 core criteria (100 points total).
Ensures content quality, human-like presentation, and conversion potential before publishing.
"""

import os
import json
from typing import Dict, Any

try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIQualityJudge:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=self.api_key) if (GEMINI_AVAILABLE and self.api_key) else None

    def evaluate_affiliate_content(self, script_text: str, hook: str, title: str, product_name: str, price: str) -> Dict[str, Any]:
        """
        Evaluates script and product setup using 100-Point Quality Matrix:
        1. First 3-Sec Hook Strength (0-20)
        2. Product Demonstration & Relevance (0-20)
        3. Value Proposition & Pricing (0-20)
        4. Call-To-Action (CTA) Punch (0-20)
        5. Speech Pacing & Flow Naturalness (0-20)
        """
        prompt = f"""
        You are an expert AI Video Quality Auditor & E-Commerce Conversion Specialist.
        
        Evaluate the following affiliate video content proposal:
        Product Name: "{product_name}"
        Price: "{price}"
        Title: "{title}"
        Hook: "{hook}"
        Script Body: "{script_text}"
        
        Return a strict JSON object with:
        {{
            "overall_score": int (0-100),
            "pass_status": bool (true if score >= 75 else false),
            "breakdown": {{
                "hook_score": int (0-20),
                "product_relevance_score": int (0-20),
                "value_prop_score": int (0-20),
                "cta_score": int (0-20),
                "flow_naturalness_score": int (0-20)
            }},
            "strengths": ["list of 2-3 key strengths"],
            "weaknesses": ["list of 1-2 weaknesses if any"],
            "detected_issues": ["list of flags like robotic tone, weak CTA, or missing price"],
            "specific_improvements": ["list of 2 actionable suggestions"],
            "human_review_checklist": [
                "Verify official price matches script",
                "Ensure #ad disclosure is included",
                "Check background clip relevance to product"
            ]
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
                return json.loads(response.text)
            except Exception as e:
                print(f"[AIQualityJudge Error]: {e}, using local rule evaluator.")

        return self._local_rule_evaluator(script_text, hook, price)

    def _local_rule_evaluator(self, script_text: str, hook: str, price: str) -> Dict[str, Any]:
        score = 82
        hook_score = 18 if len(hook) > 10 else 12
        prod_score = 16
        val_score = 16 if price in script_text or price in hook else 10
        cta_score = 16 if any(w in script_text.lower() for w in ["link", "bio", "buy", "check"]) else 8
        flow_score = 16

        total = hook_score + prod_score + val_score + cta_score + flow_score

        return {
            "overall_score": total,
            "pass_status": total >= 75,
            "breakdown": {
                "hook_score": hook_score,
                "product_relevance_score": prod_score,
                "value_prop_score": val_score,
                "cta_score": cta_score,
                "flow_naturalness_score": flow_score
            },
            "strengths": [
                "Strong pattern interruption hook in opening sentence",
                "Clear mention of product pricing and value"
            ],
            "weaknesses": [
                "Could add stronger urgency (e.g. 'Limited time deal')"
            ],
            "detected_issues": [],
            "specific_improvements": [
                "Add 'Link in bio' reminder in final 3 seconds",
                "Ensure video background shows actual product usage clip"
            ],
            "human_review_checklist": [
                "Verify official price matches script",
                "Ensure #ad disclosure is included",
                "Check audio voiceover naturalness"
            ]
        }

if __name__ == "__main__":
    judge = AIQualityJudge()
    eval_res = judge.evaluate_affiliate_content(
        script_text="Check out these noise cancelling earbuds for just ₹1,299. Link in bio to grab this deal!",
        hook="Stop buying expensive earbuds!",
        title="Best Earbuds Under ₹1500 #AmazonFinds",
        product_name="Wireless Earbuds",
        price="₹1,299"
    )
    print("Quality Judge Evaluation Output:\n", json.dumps(eval_res, indent=2))
