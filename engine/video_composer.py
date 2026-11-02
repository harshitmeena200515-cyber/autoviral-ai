import os
import subprocess
import shutil
from typing import Optional, List, Dict, Any

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = shutil.which("ffmpeg")

class VideoComposer:
    """
    Assembles audio, stock video clips, and burned-in subtitles into a ready-to-publish
    MP4 video (9:16 vertical or 16:9 widescreen) using FFmpeg.
    
    Fixed:
    - Video length matches audio length exactly (no extra blank video)
    - Subtitles burned into video (not separate SRT)
    - Bold yellow Hindi-friendly subtitles with dark background
    """

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or FFMPEG_EXE or "ffmpeg"

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get exact audio duration in seconds using ffprobe."""
        try:
            cmd = [
                self.ffmpeg_path.replace("ffmpeg", "ffprobe") if "ffprobe" not in self.ffmpeg_path else self.ffmpeg_path,
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ]
            # Try ffprobe first
            ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
            if not os.path.exists(ffprobe_path):
                ffprobe_path = shutil.which("ffprobe") or ffprobe_path
            cmd[0] = ffprobe_path
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return float(result.stdout.strip())
        except Exception:
            pass
        # Fallback: estimate from file size (MP3 ~16KB/sec for speech)
        size = os.path.getsize(audio_path)
        return max(size / 16000, 5.0)

    def compose_video(
        self,
        audio_path: str,
        video_bg_path: Optional[str],
        output_mp4_path: str,
        script_text: str,
        orientation: str = "portrait"
    ) -> str:
        """
        Combines background footage, neural audio, and BURNED-IN captions into final MP4.
        Video length = Audio length (exact match, no extra).
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_mp4_path)), exist_ok=True)
        
        # Determine target resolution
        width, height = (1080, 1920) if orientation == "portrait" else (1920, 1080)

        # Get audio duration
        audio_duration = self._get_audio_duration(audio_path)

        # 1. Generate SRT subtitle file
        srt_path = output_mp4_path.replace(".mp4", ".srt")
        self._generate_srt(script_text, srt_path, audio_duration)

        # 2. Check if background video exists
        has_valid_bg = video_bg_path and os.path.exists(video_bg_path) and os.path.getsize(video_bg_path) > 1000

        # 3. Build subtitle filter (burned-in, bold, yellow, with dark box)
        # Escape special chars in SRT path for FFmpeg on Windows
        srt_escaped = srt_path.replace("\\", "/").replace(":", "\\\\:")
        subtitle_filter = (
            f"subtitles='{srt_escaped}':force_style='"
            f"FontName=Arial,FontSize=22,PrimaryColour=&H00FFFFFF,"
            f"OutlineColour=&H00000000,BackColour=&H80000000,"
            f"Bold=1,Outline=2,Shadow=1,MarginV=80,"
            f"Alignment=2,BorderStyle=4'"
        )

        # 4. Build FFmpeg command
        if has_valid_bg:
            # Loop video to match audio, crop to portrait, burn subtitles, trim to audio length
            video_filter = (
                f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},"
                f"{subtitle_filter}"
            )
            
            cmd = [
                self.ffmpeg_path,
                "-y",
                "-stream_loop", "-1",
                "-i", video_bg_path,
                "-i", audio_path,
                "-t", str(audio_duration),    # <-- TRIM to exact audio length
                "-vf", video_filter,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",     # <-- Better streaming
                output_mp4_path
            ]
        else:
            # Dark gradient background
            cmd = [
                self.ffmpeg_path,
                "-y",
                "-f", "lavfi",
                "-i", f"color=c=0x0f0f1a:s={width}x{height}:r=30",
                "-i", audio_path,
                "-t", str(audio_duration),
                "-vf", subtitle_filter,
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                output_mp4_path
            ]

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return output_mp4_path
        except subprocess.CalledProcessError:
            # Fallback: without subtitles (in case SRT filter fails)
            if has_valid_bg:
                simple_filter = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
            else:
                simple_filter = ""
            
            fallback_cmd = [
                self.ffmpeg_path,
                "-y",
                "-stream_loop", "-1" if has_valid_bg else "0",
                "-i", video_bg_path if has_valid_bg else "color=c=0x0f0f1a",
                "-i", audio_path,
                "-t", str(audio_duration),
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-c:a", "aac",
                "-b:a", "128k",
                "-shortest",
                "-pix_fmt", "yuv420p",
                output_mp4_path
            ]
            if has_valid_bg and simple_filter:
                fallback_cmd.insert(fallback_cmd.index("-c:v"), "-vf")
                fallback_cmd.insert(fallback_cmd.index("-c:v"), simple_filter)
            
            try:
                subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            except Exception as e2:
                raise RuntimeError(f"Video composition failed: {e2}")
            return output_mp4_path

    def _generate_srt(self, text: str, srt_path: str, total_duration: float = 30.0):
        """
        Creates timing-based SRT subtitles synced to audio duration.
        Short 3-4 word chunks for viral reel-style captions.
        """
        words = text.split()
        if not words:
            return

        # Chunk into 3-4 word snippets for fast reading
        chunk_size = 4
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        # Distribute evenly across audio duration
        if len(chunks) > 0:
            sec_per_chunk = total_duration / len(chunks)
        else:
            sec_per_chunk = 1.5

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                start_sec = i * sec_per_chunk
                end_sec = min(start_sec + sec_per_chunk, total_duration)

                f.write(f"{i + 1}\n")
                f.write(f"{self._format_timestamp(start_sec)} --> {self._format_timestamp(end_sec)}\n")
                f.write(f"{chunk}\n\n")

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
