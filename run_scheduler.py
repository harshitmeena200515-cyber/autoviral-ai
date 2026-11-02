"""
Standalone Background Auto-Pilot Worker
Runs in background, monitors configured posting times (e.g. 12:30 PM & 7:00 PM),
and triggers the automated video creation & upload cycle.
"""

import time
import datetime
import sys
from dotenv import load_dotenv

load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from engine.daily_scheduler import DailyScheduler


def main():
    print("=" * 60)
    print("🚀 AutoViral AI — Daily Auto-Pilot Background Worker Started")
    print("=" * 60)

    last_run_day = None

    while True:
        try:
            config = DailyScheduler.load_config()
            if not config.get("enabled", False):
                time.sleep(30)
                continue

            now = datetime.datetime.now()
            current_time_str = now.strftime("%H:%M")
            current_day_str = now.strftime("%Y-%m-%d")

            post_times = config.get("post_times", ["12:30", "19:00"])

            # Check if current time matches any post time
            if current_time_str in post_times:
                run_key = f"{current_day_str}_{current_time_str}"
                if config.get("last_run_slot") != run_key:
                    print(f"⏰ Triggering scheduled auto-pilot run for slot: {run_key}")
                    config["last_run_slot"] = run_key
                    DailyScheduler.save_config(config)

                    res = DailyScheduler.execute_autopilot_cycle(
                        niche=config.get("niche", "Technology"),
                        language=config.get("language", "Hinglish"),
                        voice=config.get("voice", "Hindi Male (Madhur)"),
                        speed=config.get("speed", "+10%"),
                        youtube_privacy=config.get("youtube_privacy", "private")
                    )
                    print(f"✅ Auto-pilot run finished: {res['status']}")

            time.sleep(30)
        except KeyboardInterrupt:
            print("Stopping auto-pilot worker...")
            break
        except Exception as e:
            print(f"Worker exception: {e}")
            time.sleep(30)


if __name__ == "__main__":
    main()
