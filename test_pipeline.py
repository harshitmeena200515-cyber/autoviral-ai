import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from engine.algorithm_analyzer import AlgorithmAnalyzer
from engine.audio_engine import AudioEngine
from engine.thumbnail_engine import ThumbnailEngine
from engine.video_composer import VideoComposer
from engine.script_generator import ScriptGenerator

print("Testing AutoViral AI Core Modules...")

# 1. Test Script Generator & Algorithm Analyzer
script_gen = ScriptGenerator()
result = script_gen.generate("3 Secret AI Coding Tools", language="Hindi")
print("[✓] Script Generated:", result.get("hook"))

analyzer = AlgorithmAnalyzer()
analysis = analyzer.analyze_script(
    result.get("voiceover_script", ""),
    result.get("hook", ""),
    result.get("title_suggestions", ["Default Title"])[0]
)
print("[✓] Algorithm Virality Score:", analysis["total_score"], "-", analysis["virality_grade"])

# 2. Test Audio Engine (Edge-TTS Hindi Voice)
audio_engine = AudioEngine()
test_audio_path = os.path.join("output", "test_audio.mp3")
audio_engine.generate_speech(
    text="नमस्ते दोस्तों! आज हम जानेंगे कोडिंग के तीन सबसे बड़े सीक्रेट्स।",
    output_path=test_audio_path,
    voice_name="Hindi Male (Madhur)"
)
print("[✓] Audio Generated successfully:", test_audio_path, f"({os.path.getsize(test_audio_path)} bytes)")

# 3. Test Thumbnail Engine
test_thumb_path = os.path.join("output", "test_thumb.jpg")
ThumbnailEngine.create_thumbnail(
    title_text="3 AI CODING SECRETS!",
    output_path=test_thumb_path,
    format_type="Shorts (9:16)"
)
print("[✓] Thumbnail Generated successfully:", test_thumb_path, f"({os.path.getsize(test_thumb_path)} bytes)")

# 4. Test Video Composer with procedural background & audio
test_video_path = os.path.join("output", "test_video.mp4")
composer = VideoComposer()
composer.compose_video(
    audio_path=test_audio_path,
    video_bg_path=None, # Procedural background
    output_mp4_path=test_video_path,
    script_text="नमस्ते दोस्तों! आज हम जानेंगे कोडिंग के तीन सबसे बड़े सीक्रेट्स।"
)
print("[✓] Video Composed successfully:", test_video_path, f"({os.path.getsize(test_video_path)} bytes)")

print("\n🎉 ALL CORE PIPELINE TESTS PASSED!")
