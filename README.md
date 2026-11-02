# 🚀 AutoViral AI

**Autonomous YouTube Shorts & Instagram Reels Generator**

AutoViral AI is a zero-cost, fully automated AI platform that generates viral short-form videos — complete with AI-written scripts, neural voiceovers, stock footage, burned-in captions, and high-CTR thumbnails. Built-in human review ensures zero AI hallucinations before publishing.

---

## ✨ Features

- 🧠 **AI Script Engine** — Google Gemini generates 3-second hooks and high-retention scripts optimized for short-form virality.
- 🎙️ **Neural Voiceover** — Zero-cost natural speech via `edge-tts` with Hindi & English voices (Madhur, Swara, Prabhat).
- 🎬 **Automated Video Assembly** — Stitches stock clips, audio, and burned-in captions using FFmpeg.
- 🖼️ **Clickable Thumbnails** — High-CTR cover cards with gradient backgrounds and bold typography.
- 📈 **Algorithm Analyzer** — Evaluates Retention potential, Hook strength, and View-vs-Swipe-Away (VVSA) metrics.
- 🛡️ **Human Review Dashboard** — Real-time review & edit screen to inspect and tweak scripts before rendering.
- 📤 **YouTube & Instagram Publishing** — Upload directly to YouTube Shorts with metadata, or export for Instagram Reels.
- 🤖 **Autopilot Mode** — One-click daily scheduler generates a fresh reel on its own.
- 🌐 **Free Hosting Ready** — Deployable on Streamlit Community Cloud with a free `.streamlit.app` domain.

---

## 🛠️ Setup Instructions

### Prerequisites

- **Python 3.10+**
- **FFmpeg** (bundled via `imageio-ffmpeg`, no manual install needed)
- **Git** (optional, for cloning)

### 1. Install Dependencies

```powershell
cd "C:\Users\Harshit Meena\.gemini\antigravity\scratch\autoviral-ai"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file and add your keys:

```powershell
copy .env.example .env
```

Edit `.env` and fill in your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here
```

> [!TIP]
> You can also enter API keys directly in the Streamlit app sidebar — no `.env` file required.

---

## 🚀 How to Run

### Option 1: Streamlit Web App

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

### Option 2: One-Click Batch File

Double-click **`GENERATE_NEW_REEL.bat`** on your Desktop. It runs the autopilot pipeline, saves the video to `output/`, copies it to Downloads for easy sharing, and opens the output folder.

---

## 🔑 API Keys Needed

| Service | Cost | Purpose | Get It |
|---------|------|---------|--------|
| **Google Gemini** | ✅ Free | AI script generation | [aistudio.google.com](https://aistudio.google.com) |
| **Pexels** | ✅ Free | HD stock video clips | [pexels.com/api](https://www.pexels.com/api/) |
| **YouTube Data API** | ✅ Free (optional) | Direct upload to YouTube Shorts | [console.cloud.google.com](https://console.cloud.google.com) |

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **AI Brain** | Google Gemini (via `google-genai`) |
| **Voiceover** | Edge TTS (`edge-tts`) |
| **Video Rendering** | FFmpeg (via `imageio-ffmpeg`) |
| **Thumbnails** | Pillow |
| **Stock Footage** | Pexels API |
| **YouTube Upload** | Google API Client |
| **Config** | `python-dotenv` |

---

## 📁 Directory Structure

```
autoviral-ai/
├── app.py                    # Streamlit web application (main entry point)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not committed)
├── .env.example              # Template for .env
├── autopilot_config.json     # Autopilot scheduler settings
├── run_scheduler.py          # CLI scheduler runner
├── start.bat                 # Quick-start batch file
├── test_pipeline.py          # Pipeline tests
├── engine/                   # Core engine modules
│   ├── ai_brain.py           # Gemini AI integration
│   ├── script_generator.py   # Script generation logic
│   ├── audio_engine.py       # Edge TTS voiceover
│   ├── video_fetcher.py      # Pexels stock video downloader
│   ├── video_composer.py     # FFmpeg video assembly
│   ├── thumbnail_engine.py   # Thumbnail/cover card generator
│   ├── algorithm_analyzer.py # Virality & retention scoring
│   ├── quality_judge.py      # Content quality evaluation
│   ├── daily_scheduler.py    # Autopilot daily pipeline
│   ├── upload_manager.py     # Upload orchestration
│   ├── youtube_publisher.py  # YouTube Shorts uploader
│   ├── youtube_analytics.py  # YouTube analytics tracker
│   ├── instagram_analytics.py# Instagram insights
│   ├── omni_publisher.py     # Multi-platform publisher
│   ├── omni_algo_brain.py    # Cross-platform algorithm brain
│   ├── affiliate_engine.py   # Affiliate link integration
│   └── account_setup_helper.py # Account setup wizard
├── data/                     # Cached data & assets
└── output/                   # Generated videos saved here
```

---

## 📄 License

This project is for personal use.
