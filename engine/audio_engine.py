import asyncio
import os
from typing import Optional, List, Dict

try:
    import edge_tts
except ImportError:
    edge_tts = None

class AudioEngine:
    """
    Generates high quality neural voiceovers using Edge-TTS for free (no API key needed).
    Supports natural Hindi, Indian English, and Global English voices.
    """

    VOICES: Dict[str, str] = {
        "Hindi Male (Madhur)": "hi-IN-MadhurNeural",
        "Hindi Female (Swara)": "hi-IN-SwaraNeural",
        "Indian English Male (Prabhat)": "en-IN-PrabhatNeural",
        "Indian English Female (Neerja)": "en-IN-NeerjaNeural",
        "US English Male (Christopher)": "en-US-ChristopherNeural",
        "US English Female (Jenny)": "en-US-JennyNeural"
    }

    def __init__(self, default_voice: str = "hi-IN-MadhurNeural"):
        self.default_voice = default_voice

    async def _generate_async(self, text: str, voice: str, output_path: str, rate: str = "+10%") -> str:
        """
        Async call to Edge-TTS. Rate +10% gives optimal energetic pacing for reels/shorts.
        """
        if not edge_tts:
            raise ImportError("edge-tts library is not installed.")

        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
        await communicate.save(output_path)
        return output_path

    def generate_speech(self, text: str, output_path: str, voice_name: Optional[str] = None, speed: str = "+10%") -> str:
        """
        Synchronous wrapper to generate audio file.
        """
        voice = self.VOICES.get(voice_name, voice_name) or self.default_voice
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Clean text of markdown or special characters before speaking
        clean_text = text.replace("*", "").replace("#", "").replace("`", "").replace('"', '').strip()
        
        import subprocess, sys, time
        venv_bin = os.path.join(os.path.dirname(sys.executable), "edge-tts.exe")
        cmd = [venv_bin if os.path.exists(venv_bin) else "edge-tts", "--voice", voice, "--rate", speed, "--text", clean_text, "--write-media", output_path]

        for attempt in range(3):
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
                    return output_path
            except Exception:
                time.sleep(2)

        return output_path

    @classmethod
    def get_available_voices(cls) -> List[str]:
        return list(cls.VOICES.keys())
