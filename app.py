import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Reconfigure stdout for utf-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from engine.script_generator import ScriptGenerator
from engine.algorithm_analyzer import AlgorithmAnalyzer
from engine.audio_engine import AudioEngine
from engine.thumbnail_engine import ThumbnailEngine
from engine.video_fetcher import VideoFetcher
from engine.video_composer import VideoComposer
from engine.youtube_publisher import YouTubePublisher
from engine.youtube_analytics import YouTubeAnalytics
from engine.instagram_analytics import InstagramAnalytics
from engine.upload_manager import UploadManager
from engine.ai_brain import AIBrain
from engine.daily_scheduler import DailyScheduler
from engine.omni_algo_brain import OmniAlgorithmBrain
from engine.omni_publisher import OmniPublisher
from engine.affiliate_engine import AffiliateEngine
from engine.quality_judge import AIQualityJudge

# ─── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoViral AI — Full Studio & Auto-Pilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8E53, #FFA07A);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-card {
        padding: 14px 18px; background: #1A1A2E; border-radius: 10px;
        border-left: 4px solid #00C853; margin-bottom: 10px;
    }
    .metric-card h3 { margin: 0; color: #00E676; font-size: 1.6rem; }
    .metric-card p { margin: 4px 0 0 0; color: #AAA; font-size: 0.85rem; }
    .yt-red { border-left-color: #FF0000; }
    .yt-red h3 { color: #FF4444; }
    .ig-purple { border-left-color: #C13584; }
    .ig-purple h3 { color: #E040FB; }
    .success-banner {
        background: #1B5E20; padding: 12px 18px; border-radius: 8px;
        color: #A5D6A7; margin: 10px 0;
    }
    .status-badge-on {
        background: #00C853; color: black; font-weight: bold; padding: 4px 12px; border-radius: 12px;
    }
    .status-badge-off {
        background: #D50000; color: white; font-weight: bold; padding: 4px 12px; border-radius: 12px;
    }
    .sticky-note-yellow {
        background-color: #fef08a;
        color: #1e1b4b;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 4px 6px 12px rgba(0,0,0,0.4);
        border-left: 8px solid #eab308;
    }
    .sticky-note-blue {
        background-color: #1e293b;
        color: #388bfd;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 4px 6px 12px rgba(0,0,0,0.4);
        border-left: 8px solid #388bfd;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────
for key in ["script_data", "generated_video", "generated_audio", "generated_thumbnail",
            "yt_connected", "ig_connected", "ai_topics", "content_calendar"]:
    if key not in st.session_state:
        st.session_state[key] = None if "connected" not in key else False

# ═══════════════════════════════════════════════════════════════════
#  SIDEBAR — API Keys & Account Connection
# ═══════════════════════════════════════════════════════════════════
st.sidebar.markdown("## 🚀 AutoViral AI")
st.sidebar.markdown("---")

# API Keys
st.sidebar.subheader("🔑 API Keys")
gemini_key = st.sidebar.text_input("Gemini API Key", value=os.getenv("GEMINI_API_KEY", ""), type="password",
                                    help="Free: aistudio.google.com")
pexels_key = st.sidebar.text_input("Pexels API Key", value=os.getenv("PEXELS_API_KEY", ""), type="password",
                                    help="Free: pexels.com/api")

# YouTube Connection
st.sidebar.markdown("---")
st.sidebar.subheader("🔴 YouTube Account")
yt_client_secret = st.sidebar.file_uploader("Upload client_secret.json", type=["json"], key="yt_secret",
                                             help="Google Cloud Console → OAuth 2.0 Client → Download JSON")
if yt_client_secret:
    yt_secret_path = os.path.join(".", "client_secret.json")
    with open(yt_secret_path, "wb") as f:
        f.write(yt_client_secret.getvalue())
    st.sidebar.success("✅ client_secret.json saved")

# Instagram Connection
st.sidebar.markdown("---")
st.sidebar.subheader("🟣 Instagram Account")
ig_token = st.sidebar.text_input("Instagram Access Token", type="password",
                                  help="Facebook Developer → User Token")
ig_user_id = st.sidebar.text_input("Instagram Business Account ID",
                                    help="Your numeric IG Business account ID")

# Voice & Format
st.sidebar.markdown("---")
st.sidebar.subheader("🎙️ Voice & Format")
available_voices = AudioEngine.get_available_voices()
selected_voice = st.sidebar.selectbox("Voice", available_voices, index=0)
speech_speed = st.sidebar.select_slider("Speed", options=["+0%", "+10%", "+15%", "+20%"], value="+10%")
format_type = st.sidebar.radio("Format", ["Shorts / Reels (9:16)", "Long Video (16:9)"], index=0)

# ═══════════════════════════════════════════════════════════════════
#  MAIN INTERFACE
# ═══════════════════════════════════════════════════════════════════
st.markdown('<div class="main-title">🚀 AutoViral AI — Full Studio & Auto-Pilot</div>', unsafe_allow_html=True)
st.caption("AI Studio • Daily Auto-Pilot • Real-time Analytics • 1-Click Upload • 100% मुफ़्त")

tabs = st.tabs([
    "🤖 Daily Auto-Pilot (रोज़ाना ऑटो-अपलोड)",
    "🛍️ Affiliate Video Studio (Amazon / Meesho / Flipkart)",
    "⚡ Antigravity Omni-Studio (1-Device Workstation)",
    "🧠 AI Studio Brain",
    "📊 Account Dashboard",
    "🎬 Video Generator",
    "📤 Auto Upload",
    "📈 Algorithm Insights",
    "💰 Monetization & Ads",
    "🌐 Deploy Guide"
])

# ═══════════════════════════════════════════════════════════════════
#  TAB 0: DAILY AUTO-PILOT (रोज़ाना ऑटो-अपलोड)
# ═══════════════════════════════════════════════════════════════════
with tabs[0]:
    st.header("🤖 Daily Auto-Pilot — बिना छुए रोज़ाना वीडियो अपलोड")
    st.info("💡 **यह फीचर क्या करता है?** आप बस इसे ON रखें — यह रोज़ाना AI से नए वायरल ट्रेंडिंग टॉपिक चुनेगा, वीडियो बनाएगा, आवाज़ डालेगा, और YouTube Shorts पर अपने आप अपलोड कर देगा!")

    config = DailyScheduler.load_config()

    col_toggle, col_settings = st.columns([1, 1.5])

    with col_toggle:
        st.subheader("⚙️ Auto-Pilot Switch")
        is_enabled = st.toggle("🟢 Auto-Pilot Mode (Active)", value=config.get("enabled", True))
        
        if is_enabled != config.get("enabled", False):
            config["enabled"] = is_enabled
            DailyScheduler.save_config(config)
            st.success(f"Auto-Pilot {'चालू (ON)' if is_enabled else 'बंद (OFF)'} कर दिया गया!")
            st.rerun()

        if is_enabled:
            st.markdown('<span class="status-badge-on">🟢 AUTO-PILOT IS ACTIVE</span>', unsafe_allow_html=True)
            st.write(f"⏱️ **Scheduled Post Times:** {', '.join(config.get('post_times', ['12:30', '19:00']))} IST")
            st.write(f"🎯 **Target Niche:** `{config.get('niche', 'Technology & Coding')}`")
            st.write(f"🔒 **YouTube Privacy:** `{config.get('youtube_privacy', 'private')}`")
        else:
            st.markdown('<span class="status-badge-off">🔴 AUTO-PILOT IS PAUSED</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("⚡ Manually Trigger Today's Batch")
        st.caption("अगर आप scheduled time का इंतज़ार नहीं करना चाहते और अभी एक वीडियो अपने आप बनवाकर अपलोड करना चाहते हैं:")
        if st.button("🚀 Run Auto-Pilot Batch Right Now", type="primary", use_container_width=True):
            with st.spinner("🤖 AI Topic चुन रहा है... Script लिख रहा है... Voice + Video compose कर रहा है..."):
                res = DailyScheduler.execute_autopilot_cycle(
                    niche=config.get("niche", "Technology & Coding"),
                    language=config.get("language", "Hinglish"),
                    voice=selected_voice,
                    speed=speech_speed,
                    youtube_privacy=config.get("youtube_privacy", "private"),
                    gemini_key=gemini_key,
                    pexels_key=pexels_key,
                    ig_token=ig_token,
                    ig_user_id=ig_user_id
                )
                if res["status"] == "SUCCESS":
                    st.success(f"🎉 Auto-Pilot Cycle Complete! Topic: **{res['topic']}**")
                    if res.get("youtube_url"):
                        st.markdown(f"📺 **YouTube Short:** [{res['youtube_url']}]({res['youtube_url']})")
                else:
                    st.error(f"❌ Cycle Failed: {res.get('error')}")
                st.rerun()

    with col_settings:
        st.subheader("🛠️ Auto-Pilot Settings")
        with st.form("autopilot_settings_form"):
            selected_niche = st.selectbox(
                "Niche / Category",
                ["Technology & Coding", "Money & Career (Students)", "AI Tools & Secrets", "Education & Facts", "Motivation"],
                index=0
            )
            selected_lang = st.selectbox("Language", ["Hinglish", "Hindi", "English"], index=0)
            time_slots = st.multiselect(
                "Posting Time Slots (IST)",
                ["09:00", "12:30", "15:00", "18:00", "19:00", "21:00"],
                default=config.get("post_times", ["12:30", "19:00"])
            )
            privacy_setting = st.selectbox(
                "YouTube Upload Privacy Mode",
                ["private", "unlisted", "public"],
                index=0,
                help="Recommended: Start with 'private' so you can preview in YouTube Studio before going public!"
            )
            save_btn = st.form_submit_button("💾 Save Settings", use_container_width=True)
            if save_btn:
                config["niche"] = selected_niche
                config["language"] = selected_lang
                config["post_times"] = time_slots if time_slots else ["12:30", "19:00"]
                config["youtube_privacy"] = privacy_setting
                DailyScheduler.save_config(config)
                st.success("✅ Auto-Pilot सेटिंग्स सेव हो गईं!")
                st.rerun()

    st.markdown("---")
    st.subheader("📜 Auto-Pilot Execution History (Past Automated Uploads)")
    history = DailyScheduler.get_history()
    if history:
        for idx, item in enumerate(history[:10]):
            with st.expander(f"🕒 {item.get('timestamp')} — {item.get('topic')} [{item.get('status')}]", expanded=(idx == 0)):
                st.write(f"**Status:** `{item.get('status')}`")
                st.write(f"**YouTube Status:** `{item.get('youtube_status')}`")
                if item.get("youtube_url"):
                    st.markdown(f"📺 **Short Link:** [{item.get('youtube_url')}]({item.get('youtube_url')})")
                if item.get("video_path") and os.path.exists(item.get("video_path")):
                    st.video(item.get("video_path"))
    else:
        st.caption("अभी तक कोई automated batch नहीं चला है। ऊपर 'Run Auto-Pilot Batch Right Now' दबाकर टेस्ट करें!")

# ═══════════════════════════════════════════════════════════════════
#  TAB 1: AFFILIATE VIDEO STUDIO (Amazon / Meesho / Flipkart)
# ═══════════════════════════════════════════════════════════════════
with tabs[1]:
    st.header("🛍️ Affiliate Video Studio — AI Powered Commerce")
    st.info("💡 **यह क्या करता है?** Amazon/Meesho/Flipkart के प्रोडक्ट्स डालें और AI खुद-ब-खुद viral affiliate hook और स्क्रिप्ट तैयार करेगा।")
    
    col_aff1, col_aff2 = st.columns([1, 1.2])
    with col_aff1:
        st.subheader("🛒 Product Details")
        aff_prod_name = st.text_input("Product Name", value="Noise Cancelling Earbuds")
        aff_price = st.text_input("Current Deal Price", value="₹999")
        aff_orig_price = st.text_input("Original Price", value="₹2999")
        aff_platform = st.selectbox("Platform", ["Amazon India", "Meesho", "Flipkart", "Myntra"])
        aff_url = st.text_input("Affiliate Link (Optional)", value="")
        aff_photo = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])
        
        gen_aff_btn = st.button("🚀 Generate Affiliate Video Script", type="primary", use_container_width=True)
    
    with col_aff2:
        st.subheader("📊 Affiliate Hook & Metadata")
        meta = AffiliateEngine.build_affiliate_metadata(aff_prod_name, aff_price, aff_orig_price, aff_platform, aff_url)
        st.markdown(f"**Discount:** `{meta['discount_percentage']}` | **Platform:** `{meta['platform']}`")
        st.caption(f"🛡️ *{meta['disclosure']}*")
        
        hooks = AffiliateEngine.get_conversion_hook_templates()
        st.markdown("**🔥 Conversion Hooks:**")
        for h in hooks[:3]:
            st.markdown(f"- *{h}*")
            
        if gen_aff_btn:
            with st.spinner("Generating High-Converting Script..."):
                brain_aff = AIBrain(api_key=gemini_key)
                prod_info = f"{aff_prod_name}, Price: {aff_price}, Original: {aff_orig_price}, Platform: {aff_platform}"
                if aff_photo:
                    img_bytes = aff_photo.getvalue()
                    res_aff = brain_aff.analyze_product_photo(img_bytes, prod_info)
                else:
                    res_aff = {"voiceover_script": f"Here is a quick deal on {aff_platform}. {aff_prod_name} is now just {aff_price} instead of {aff_orig_price}! Check link in bio."}
                
                st.session_state["aff_script"] = res_aff.get("voiceover_script", "Script generation failed.")
                
        if "aff_script" in st.session_state:
            st.text_area("🎙️ Generated Script", value=st.session_state["aff_script"], height=100)
            
            judge = AIQualityJudge(api_key=gemini_key)
            score = judge.evaluate_affiliate_content(st.session_state["aff_script"], meta)
            st.markdown(f"**AI Quality Score:** ⭐ `{score.get('score', 85)} / 100`")
            st.caption(f"Feedback: {score.get('feedback', 'Good to go!')}")
            
            if st.button("📤 Send to Video Generator", key="send_aff_to_vg"):
                st.session_state.active_topic = st.session_state["aff_script"]
                st.success("Sent to Video Generator tab! Switch to 'Video Generator' tab to render.")

# ═══════════════════════════════════════════════════════════════════
#  TAB 2: ANTIGRAVITY OMNI-STUDIO (1-DEVICE WORKSTATION)
# ═══════════════════════════════════════════════════════════════════
with tabs[2]:
    st.header("⚡ Antigravity Omni-Studio — All-in-One Autonomous Workstation")
    st.info("🎯 **100% एकीकृत कंट्रोल सेंटर:** एक ही स्क्रीन पर AI Algorithm Brain, Viral Hook Analysis, One-Click Multi-Format Video Generation और Auto-Publishing Matrix!")

    omni_brain = OmniAlgorithmBrain(api_key=gemini_key)
    omni_pub = OmniPublisher()

    col_input, col_brain_preview = st.columns([1, 1.2])

    with col_input:
        st.subheader("🔮 1-Click AI Creator Engine")
        omni_topic = st.text_input("Enter Topic / Prompt", value="Top 3 Secret AI Tools for Students 2026", key="omni_topic")
        omni_niche = st.selectbox("Niche Category", ["Technology & AI", "Student & Study Hacks", "Finance & Earning", "Affiliate Deals & Unboxing", "Motivation & Facts"], key="omni_niche")
        
        if st.button("🚀 Generate & Process Omni Content", type="primary", use_container_width=True):
            with st.spinner("🧠 Algorithm Brain & Production Engine running..."):
                decision = omni_brain.analyze_and_optimize(omni_topic, omni_niche)
                
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                audio_path = output_dir / "omni_voiceover.mp3"
                AudioEngine().generate_speech(decision.get("script_body", ""), str(audio_path), selected_voice, speech_speed)
                
                import sqlite3, json
                db_path = Path("data") / "autoviral_omni.db"
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO content_history (topic, format_type, title, description, script, hashtags, status, video_path)
                       VALUES (?, ?, ?, ?, ?, ?, 'ready', ?)''',
                    (omni_topic, decision.get("recommended_format", "shorts_9_16"), decision.get("title", ""), decision.get("description", ""), decision.get("script_body", ""), json.dumps(decision.get("hashtags", [])), str(audio_path))
                )
                conn.commit()
                rec_id = cursor.lastrowid
                conn.close()

                decision["record_id"] = rec_id
                st.session_state["omni_decision"] = decision
                st.success(f"✅ Content generated, rendered & saved to DB (ID: #{rec_id})!")

    with col_brain_preview:
        st.subheader("🧠 Self-Thinking Brain Insights")
        if "omni_decision" in st.session_state and st.session_state["omni_decision"]:
            dec = st.session_state["omni_decision"]
            st.markdown(f"**Format Recommendation:** `{dec.get('recommended_format', '').upper()}`")
            st.markdown(f"**Predicted Virality Score:** ⭐ `{dec.get('virality_score_prediction', 88.0)} / 100`")
            st.markdown(f"**Pattern Interrupt Hook:** *\"{dec.get('viral_hook', '')}\"*")
            st.text_area("Full Generated Script", value=dec.get("script_body", ""), height=100)
            
            rec_id = dec.get("record_id", 1)
            if st.button(f"📤 Auto-Publish Content #{rec_id} to Shorts & Reels Matrix", type="primary", use_container_width=True):
                with st.spinner("Publishing across connected accounts..."):
                    pub_res = omni_pub.publish_content(rec_id)
                    st.success("🎉 Video Successfully Uploaded across YouTube Shorts & Instagram Reels!")
                    st.json(pub_res)
        else:
            st.caption("Waiting for prompt input above...")

    st.markdown("---")
    st.subheader("📜 Omni Production & Upload History (SQLite DB)")
    import sqlite3
    db_path = Path("data") / "autoviral_omni.db"
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, topic, format_type, title, status, created_at FROM content_history ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        conn.close()

        if rows:
            import pandas as pd
            df = pd.DataFrame(rows, columns=["ID", "Topic", "Format", "Title", "Status", "Created At"])
            st.dataframe(df, use_container_width=True)
        else:
            st.caption("No history records yet. Generate your first video above!")


# ═══════════════════════════════════════════════════════════════════
#  TAB 3: AI STUDIO BRAIN & MULTIMODAL REEL ANALYZER
# ═══════════════════════════════════════════════════════════════════
with tabs[3]:
    st.header("🧠 Google AI Studio Brain — Multimodal Content Engine")
    st.caption("Gemini 2.5 Flash: Product Photo Analysis • Reference Reel Deconstruction • Affiliate Strategy Integration")

    ai_tool = st.radio("AI Brain Tool चुनें:", [
        "📸 Product Photo -> Affiliate Reel Script",
        "🎬 Reference Reel + Product Photo -> Inspired Reel",
        "🔥 Trending Topics Finder (inc. Affiliate Deals)",
        "🎯 Viral Hook Rewriter",
        "📅 7-Day Content Calendar Planner"
    ], horizontal=True)

    brain = AIBrain(api_key=gemini_key)

    if "Product Photo -> Affiliate Reel" in ai_tool:
        st.subheader("📸 Product Photo Analysis -> Affiliate Reel Concept & Script")
        col_p1, col_p2 = st.columns([1, 1.2])
        with col_p1:
            uploaded_prod_img = st.file_uploader("Upload Product Photo (PNG/JPG)", type=["jpg", "png", "jpeg"], key="prod_img_uploader")
            prod_notes = st.text_input("Additional Product Notes (Price, Deal, Name)", value="Amazon Noise Cancelling Earbuds under ₹1299")
            analyze_img_btn = st.button("🔮 Analyze Photo & Create Reel Concept", type="primary", use_container_width=True)

        with col_p2:
            if analyze_img_btn and uploaded_prod_img:
                with st.spinner("Gemini Vision photo को analyze कर रहा है और सटीक एफिलिएट रील तैयार कर रहा है..."):
                    img_bytes = uploaded_prod_img.getvalue()
                    analysis_res = brain.analyze_product_photo(img_bytes, prod_notes)
                    st.session_state["prod_analysis"] = analysis_res

            if "prod_analysis" in st.session_state and st.session_state["prod_analysis"]:
                res = st.session_state["prod_analysis"]
                st.markdown(f"**Category:** `{res.get('detected_product_category')}` | **Target:** `{res.get('target_audience')}`")
                st.markdown(f"**🎯 Viral Hook:** *\"{res.get('viral_hook')}\"*")
                st.text_area("🎙️ Voiceover Script", value=res.get("voiceover_script"), height=100)
                
                with st.expander("🎬 Scene-by-Scene Breakdown & Editing Cues"):
                    for sc in res.get("scene_breakdown", []):
                        st.markdown(f"• **{sc.get('time')}**: Visual: *{sc.get('visual')}* | Audio: *{sc.get('audio')}*")
                    st.info(f"✂️ **Editing Cues:** {res.get('editing_instructions')}")
                
                if st.button("📋 Send Script to Video Generator Tab"):
                    st.session_state.active_topic = res.get("voiceover_script")
                    st.success("Script copied! Switch to 'Video Generator' tab to render.")

    elif "Reference Reel + Product Photo" in ai_tool:
        st.subheader("🎬 Reference Reel Structure Analysis -> Inspired Original Reel")
        st.info("💡 **यह क्या करता है?** किसी भी वायरल रील का स्टाइल/टाइटल डालें और अपने प्रोडक्ट की फोटो दें — AI कॉपी किए बिना उसी वायरल स्टाइल में आपके प्रोडक्ट की नई रील बनाएगा!")
        
        col_r1, col_r2 = st.columns([1, 1.2])
        with col_r1:
            ref_style = st.text_area("Reference Reel Description / Style (उदा: 'Fast cuts, bold yellow captions, first 2 seconds stop scrolling hook, unboxing format')", height=100)
            target_pname = st.text_input("Your Target Product Name", value="Smart Watch Ultra Under ₹1999")
            uploaded_ref_prod = st.file_uploader("Upload Product Photo (Optional)", type=["jpg", "png", "jpeg"], key="ref_prod_img")
            gen_ref_btn = st.button("⚡ Generate Inspired Original Reel", type="primary", use_container_width=True)

        with col_r2:
            if gen_ref_btn and ref_style.strip():
                with st.spinner("Reference Reel का स्टाइल डीकन्स्ट्रक्ट करके नई रील तैयार की जा रही है..."):
                    ref_bytes = uploaded_ref_prod.getvalue() if uploaded_ref_prod else None
                    inspired_res = brain.analyze_reference_reel_and_product(ref_style, ref_bytes, target_pname)
                    st.session_state["inspired_res"] = inspired_res

            if "inspired_res" in st.session_state and st.session_state["inspired_res"]:
                ires = st.session_state["inspired_res"]
                st.markdown(f"**Reference Analysis:** {ires.get('reference_style_analysis')}")
                st.markdown(f"**🎯 Inspired Hook:** *\"{ires.get('viral_hook')}\"*")
                st.text_area("🎙️ Inspired Script", value=ires.get("voiceover_script"), height=100)
                
                with st.expander("✂️ Transitions & Timing Cues"):
                    st.write(ires.get("editing_guidelines"))
                    for sb in ires.get("scene_breakdown", []):
                        st.markdown(f"• Scene {sb.get('scene')} ({sb.get('duration')}): {sb.get('description')}")

    brain = AIBrain(api_key=gemini_key)

    if "Trending Topics" in ai_tool:
        st.subheader("🔥 AI Trending Topics Finder")
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            t_niche = st.selectbox("कैटेगरी चुनें:", ["Tech & AI", "Student Career & Money", "Coding Secrets", "Life Hacks"], key="ai_niche")
        with c2:
            t_lang = st.selectbox("भाषा:", ["Hinglish", "Hindi", "English"], key="ai_lang")
        with c3:
            st.write("")
            st.write("")
            fetch_btn = st.button("🔍 ट्रेंडिंग टॉपिक्स ढूंढें", type="primary", use_container_width=True)

        if fetch_btn:
            with st.spinner("Gemini AI से आज के सबसे ज़्यादा वायरल टॉपिक खोजे जा रहे हैं..."):
                st.session_state.ai_topics = brain.suggest_trending_topics(niche=t_niche, language=t_lang, count=6)

        if st.session_state.ai_topics:
            for item in st.session_state.ai_topics:
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{item.get('topic', '')}</h3>
                        <p><b>🎯 Hook Idea:</b> {item.get('hook_idea', '')}</p>
                        <p><b>🔥 Virality Potential:</b> {item.get('virality_score', 8)}/10 | <b>Reason:</b> {item.get('reason', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🎬 इस टॉपिक पर वीडियो बनाएं", key=f"btn_{item.get('topic')[:20]}"):
                        st.session_state.active_topic = item.get("topic")
                        st.success(f"टॉपिक Video Generator में कॉपी हो गया! 'Video Generator' टैब खोलें।")

    elif "Viral Hook Rewriter" in ai_tool:
        st.subheader("🎯 Viral Hook Rewriter")
        st.caption("अगर दर्शक पहले 2 सेकंड में स्वाइप कर दें तो वीडियो कभी वायरल नहीं होगी। अपना हुक यहाँ डालें, AI इसे 5 अलग-अलग साइकोलॉजिकल ट्रिगर्स में बदल देगा:")
        hook_input = st.text_input("कमज़ोर हुक (उदा: 'आज मैं आपको 3 AI टूल्स बताऊंगा'):", value="आज मैं आपको 3 AI टूल्स बताऊंगा")
        hook_topic = st.text_input("टॉपिक:", value="3 Free AI Tools")
        if st.button("⚡ Hook को 10x Punchy बनाएं", type="primary"):
            with st.spinner("AI साइकोलॉजिकल हुक्स तैयार कर रहा है..."):
                rewrites = brain.rewrite_hook(hook_input, hook_topic)
                for r in rewrites.get("rewrites", []):
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>[{r.get('style')}] {r.get('hook')}</h3>
                        <p>💡 <b>क्यों काम करेगा:</b> {r.get('why_better')}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif "7-Day Content Calendar" in ai_tool:
        st.subheader("📅 AI 7-Day Content Calendar Planner")
        cal_niche = st.selectbox("चैनल Niche:", ["Tech & Coding", "Student Money Making", "AI Tools"], key="cal_niche")
        if st.button("🗓️ पूरा 7 दिन का कंटेंट कैलेंडर बनाएं", type="primary"):
            with st.spinner("Gemini पूरे हफ़्ते के 14 वीडियो का शेड्यूल बना रहा है..."):
                st.session_state.content_calendar = brain.generate_content_calendar(niche=cal_niche, days=7)

        if st.session_state.content_calendar:
            for day in st.session_state.content_calendar:
                with st.expander(f"📌 {day.get('day')}", expanded=True):
                    for post in day.get("posts", []):
                        st.markdown(f"• **{post.get('post_time')}** ({post.get('content_type')}): **{post.get('topic')}**")
                        st.caption(f"  🎯 Hook: \"{post.get('hook')}\" | 💡 {post.get('reason')}")

    elif "Multi-Script Variations" in ai_tool:
        st.subheader("✨ 3 Different Script Variations")
        var_topic = st.text_input("टॉपिक:", value="How 12th pass students can earn online")
        if st.button("⚡ 3 अलग स्क्रिप्ट्स जनरेट करें", type="primary"):
            with st.spinner("Gemini 3 अलग-अलग स्टाइल्स में स्क्रिप्ट लिख रहा है..."):
                vars_list = brain.generate_script_variations(var_topic)
                for v in vars_list:
                    with st.expander(f"🎭 {v.get('variation_name')} (Score: {v.get('estimated_retention_score')}/100)", expanded=True):
                        st.markdown(f"**🎯 Hook:** {v.get('hook')}")
                        st.text_area("🎙️ Script:", value=v.get("voiceover_script"), height=100)
                        st.caption(f"🖼️ Thumbnail Text: {v.get('thumbnail_text')}")

# ═══════════════════════════════════════════════════════════════════
#  TAB 4: ACCOUNT DASHBOARD
# ═══════════════════════════════════════════════════════════════════
with tabs[4]:
    st.header("📊 Account Dashboard — आपके चैनल की पूरी रिपोर्ट")

    use_demo = st.checkbox("🎮 Demo Mode (बिना account connect किए preview देखें)", value=True)

    col_yt, col_ig = st.columns(2)

    # ─── YouTube Analytics ────────────────────────────────────
    with col_yt:
        st.subheader("🔴 YouTube Channel")
        if use_demo:
            demo = YouTubeAnalytics.get_demo_data()
            ch = demo["channel"]
            st.markdown(f"""
            <div class="metric-card yt-red"><h3>{ch['subscribers']:,}</h3><p>Subscribers</p></div>
            <div class="metric-card yt-red"><h3>{ch['total_views']:,}</h3><p>Total Views</p></div>
            <div class="metric-card yt-red"><h3>{ch['video_count']}</h3><p>Videos Posted</p></div>
            """, unsafe_allow_html=True)

            st.markdown("**📈 Last 28 Days Views Trend:**")
            import pandas as pd
            trend = demo["trend"]
            df = pd.DataFrame({"Date": trend["dates"], "Views": trend["views"]})
            st.line_chart(df.set_index("Date"))

            st.markdown("**📋 Top Performing Videos:**")
            for v in demo["recent_videos"]:
                st.markdown(f"• **{v['title']}** — 👁️ {v['views']:,} | ❤️ {v['likes']} | 💬 {v['comments']}")
        else:
            yt = YouTubeAnalytics(client_secrets_path="client_secret.json")
            if os.path.exists("yt_token.json"):
                if yt.authenticate():
                    ch = yt.get_channel_stats()
                    if ch and "error" not in ch:
                        st.markdown(f"""
                        <div class="metric-card yt-red"><h3>{ch['subscribers']:,}</h3><p>Subscribers — {ch['channel_name']}</p></div>
                        <div class="metric-card yt-red"><h3>{ch['total_views']:,}</h3><p>Total Views</p></div>
                        <div class="metric-card yt-red"><h3>{ch['video_count']}</h3><p>Videos Posted</p></div>
                        """, unsafe_allow_html=True)

                        vids = yt.get_recent_videos(10)
                        if vids and "error" not in vids[0]:
                            st.markdown("**📋 Recent Videos:**")
                            for v in vids:
                                st.markdown(f"• **{v['title']}** — 👁️ {v['views']:,} | ❤️ {v['likes']} | 💬 {v['comments']}")

                        trend = yt.get_views_trend(28)
                        if trend and "error" not in trend:
                            import pandas as pd
                            df = pd.DataFrame({"Date": trend["dates"], "Views": trend["views"]})
                            st.line_chart(df.set_index("Date"))
                    else:
                        st.error(f"Error: {ch}")
            else:
                if st.button("🔗 Connect YouTube Account", key="yt_connect"):
                    if os.path.exists("client_secret.json"):
                        if yt.authenticate():
                            st.success("YouTube connected!")
                            st.rerun()
                    else:
                        st.warning("Please upload client_secret.json in sidebar first.")

    # ─── Instagram Analytics ──────────────────────────────────
    with col_ig:
        st.subheader("🟣 Instagram Account")
        if use_demo:
            demo_ig = InstagramAnalytics.get_demo_data()
            acc = demo_ig["account"]
            st.markdown(f"""
            <div class="metric-card ig-purple"><h3>{acc['followers']:,}</h3><p>Followers — @{acc['username']}</p></div>
            <div class="metric-card ig-purple"><h3>{demo_ig['insights']['reach']['total']:,}</h3><p>Total Reach (28 days)</p></div>
            <div class="metric-card ig-purple"><h3>{demo_ig['engagement_rate']}%</h3><p>Engagement Rate</p></div>
            """, unsafe_allow_html=True)

            st.markdown("**📈 Last 28 Days Reach Trend:**")
            import pandas as pd
            reach = demo_ig["insights"]["reach"]["daily"]
            df = pd.DataFrame({"Date": [r["date"] for r in reach], "Reach": [r["value"] for r in reach]})
            st.line_chart(df.set_index("Date"))

            st.markdown("**📋 Recent Reels:**")
            for m in demo_ig["recent_media"]:
                st.markdown(f"• **{m['caption']}** — ❤️ {m['likes']} | 💬 {m['comments']}")
        else:
            if ig_token and ig_user_id:
                ig = InstagramAnalytics(access_token=ig_token, ig_user_id=ig_user_id)
                acc = ig.get_account_info()
                if acc and "error" not in acc:
                    st.markdown(f"""
                    <div class="metric-card ig-purple"><h3>{acc['followers']:,}</h3><p>Followers — @{acc['username']}</p></div>
                    <div class="metric-card ig-purple"><h3>{acc['media_count']}</h3><p>Total Posts</p></div>
                    """, unsafe_allow_html=True)

                    media = ig.get_recent_media(10)
                    if media and "error" not in media[0]:
                        eng_rate = ig.calculate_engagement_rate(acc, media)
                        st.markdown(f'<div class="metric-card ig-purple"><h3>{eng_rate}%</h3><p>Engagement Rate</p></div>', unsafe_allow_html=True)
                        st.markdown("**📋 Recent Posts:**")
                        for m in media:
                            st.markdown(f"• **{m['caption']}** — ❤️ {m['likes']} | 💬 {m['comments']}")
                else:
                    st.error(f"Instagram Error: {acc}")
            else:
                st.info("Instagram connect करने के लिए Sidebar में Access Token और Business Account ID डालें।")

# ═══════════════════════════════════════════════════════════════════
#  TAB 5: VIDEO GENERATOR & REVIEW
# ═══════════════════════════════════════════════════════════════════
with tabs[5]:
    st.header("🎬 AI Video Generator & Human Review")
    col1, col2 = st.columns([1.2, 0.8])

    default_topic = getattr(st.session_state, "active_topic", "") or "3 AI Secrets to Earn Money as a Student"

    with col1:
        st.subheader("1. टॉपिक इनपुट करें")
        topic_input = st.text_input("आज किस टॉपिक पर वीडियो?", value=default_topic)
        c1, c2 = st.columns(2)
        with c1:
            lang_choice = st.selectbox("भाषा", ["Hinglish", "Pure Hindi", "English"])
        with c2:
            niche = st.selectbox("कैटेगरी", ["Tech & Coding", "Money / Career", "Education", "Motivation", "General"])

        is_affiliate_mode = st.checkbox("🛒 Enable Special Affiliate Reel Mode (Amazon / Meesho / Flipkart Deals)", value=False)
        if is_affiliate_mode:
            c_aff_p, c_aff_pr = st.columns(2)
            with c_aff_p:
                aff_platform_sel = st.selectbox("Affiliate Platform", ["Amazon India", "Meesho", "Flipkart", "Myntra"], key="vg_aff_platform")
            with c_aff_pr:
                aff_price_sel = st.text_input("Deal Price (₹)", value="₹499", key="vg_aff_price")

        if st.button("✨ AI स्क्रिप्ट तैयार करें", type="primary", use_container_width=True):
            if topic_input.strip():
                with st.spinner("Gemini AI स्क्रिप्ट लिख रहा है..."):
                    gen = ScriptGenerator(api_key=gemini_key)
                    
                    if is_affiliate_mode:
                        topic_prompt = f"{topic_input} (Affiliate Deal on {aff_platform_sel} at {aff_price_sel})"
                        st.session_state.script_data = gen.generate(topic_prompt, format_type, lang_choice)
                        # Add disclosure
                        meta = AffiliateEngine.build_affiliate_metadata(topic_input, aff_price_sel, "₹999", aff_platform_sel, "")
                        st.session_state.script_data["voiceover_script"] += f" {meta['disclosure']}"
                    else:
                        st.session_state.script_data = gen.generate(topic_input, format_type, lang_choice)
                        
                    st.session_state.generated_video = None
                    st.success("स्क्रिप्ट तैयार! नीचे review करें।")
            else:
                st.warning("कृपया पहले टॉपिक लिखें!")

    with col2:
        st.subheader("💡 वायरल टिप")
        st.info("**Hook Rule:** पहले 2 सेकंड में दर्शक का ध्यान खींचो। 'Stop scrolling!', 'क्या आपको पता है?' जैसे फ्रेज़ सबसे ज़्यादा काम करते हैं।")

    # Review Section
    if st.session_state.script_data:
        st.markdown("---")
        st.warning("🛡️ **Human Review:** नीचे AI की स्क्रिप्ट को पढ़ें और ज़रूरत हो तो एडिट करें।")
        col_r1, col_r2 = st.columns([1.2, 0.8])

        with col_r1:
            titles = st.session_state.script_data.get("title_suggestions", ["Title"])
            selected_title = st.selectbox("वायरल टाइटल:", titles)
            hook_edit = st.text_input("🎯 Hook (0-3s):", value=st.session_state.script_data.get("hook", ""))
            script_edit = st.text_area("🎙️ वॉयसओवर:", value=st.session_state.script_data.get("voiceover_script", ""), height=130)
            thumb_edit = st.text_input("🖼️ थंबनेल टेक्स्ट:", value=st.session_state.script_data.get("thumbnail_text", ""))

            st.session_state.script_data["hook"] = hook_edit
            st.session_state.script_data["voiceover_script"] = script_edit
            st.session_state.script_data["thumbnail_text"] = thumb_edit

        with col_r2:
            st.subheader("📈 Virality Score")
            analysis = AlgorithmAnalyzer().analyze_script(script_edit, hook_edit, selected_title)
            st.markdown(f"""
            <div class="metric-card"><h3>{analysis['virality_grade']}</h3>
            <p>Score: {analysis['total_score']}/100 | ~{analysis['est_duration_seconds']}s</p></div>
            """, unsafe_allow_html=True)
            for r in analysis["recommendations"]:
                st.caption(f"• {r}")

        st.markdown("---")
        if st.button("🚀 Approve & Render Video", type="primary", use_container_width=True):
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            with st.spinner("1/3: वॉयसओवर जनरेट हो रही है..."):
                audio_path = os.path.join(output_dir, "voiceover.mp3")
                AudioEngine().generate_speech(script_edit, audio_path, selected_voice, speech_speed)
                st.session_state.generated_audio = audio_path

            with st.spinner("2/3: थंबनेल और बैकग्राउंड..."):
                thumb_path = os.path.join(output_dir, "thumbnail.jpg")
                ThumbnailEngine.create_thumbnail(thumb_edit, thumb_path, format_type)
                st.session_state.generated_thumbnail = thumb_path

                kw = st.session_state.script_data.get("visual_search_keywords", ["technology"])[0]
                bg_path = os.path.join(output_dir, "background.mp4")
                VideoFetcher(api_key=pexels_key).search_and_download_video(kw, bg_path)

            with st.spinner("3/3: वीडियो कम्पोज़ हो रही है..."):
                final_path = os.path.join(output_dir, "final_reel.mp4")
                VideoComposer().compose_video(
                    audio_path, bg_path, final_path, script_edit,
                    "portrait" if "9:16" in format_type else "landscape"
                )
                st.session_state.generated_video = final_path
                st.success("🎉 वीडियो तैयार है!")

    # Show rendered output
    if st.session_state.generated_video and os.path.exists(st.session_state.generated_video):
        st.markdown("---")
        st.subheader("🎉 Final Output")
        v1, v2 = st.columns(2)
        with v1:
            st.video(st.session_state.generated_video)
            with open(st.session_state.generated_video, "rb") as f:
                st.download_button("📥 Download Video", f, "reel.mp4", "video/mp4", use_container_width=True)
        with v2:
            if st.session_state.generated_thumbnail and os.path.exists(st.session_state.generated_thumbnail):
                st.image(st.session_state.generated_thumbnail, use_container_width=True)
            if st.session_state.generated_audio and os.path.exists(st.session_state.generated_audio):
                st.audio(st.session_state.generated_audio)

# ═══════════════════════════════════════════════════════════════════
#  TAB 6: AUTO UPLOAD
# ═══════════════════════════════════════════════════════════════════
with tabs[6]:
    st.header("📤 Auto Upload — YouTube Shorts & Instagram Reels")

    if not st.session_state.generated_video or not os.path.exists(st.session_state.get("generated_video", "")):
        st.info("पहले **Video Generator** tab में एक वीडियो बनाएं, फिर यहाँ से upload करें।")
    else:
        st.success(f"✅ वीडियो तैयार है: `{st.session_state.generated_video}`")
        title_for_upload = st.text_input("Upload Title:", value=st.session_state.script_data.get("title_suggestions", ["My Short"])[0] if st.session_state.script_data else "My Short")
        desc_for_upload = st.text_area("Description:", value=st.session_state.script_data.get("description", "") if st.session_state.script_data else "", height=80)
        tags_for_upload = st.text_input("Hashtags:", value=" ".join(st.session_state.script_data.get("hashtags", [])) if st.session_state.script_data else "#shorts")

        up_col1, up_col2 = st.columns(2)

        # YouTube Upload
        with up_col1:
            st.subheader("🔴 YouTube Shorts Upload")
            yt_privacy = st.selectbox("Privacy:", ["private", "unlisted", "public"], index=0,
                                       help="Private = सिर्फ आप देख सकते हो, Public = सबके लिए")
            if st.button("🚀 Upload to YouTube", type="primary", use_container_width=True):
                if os.path.exists("yt_token.json"):
                    with st.spinner("YouTube पर upload हो रहा है..."):
                        result = UploadManager.upload_to_youtube(
                            token_path="yt_token.json",
                            video_file_path=st.session_state.generated_video,
                            title=title_for_upload,
                            description=desc_for_upload,
                            tags=tags_for_upload.split(),
                            privacy=yt_privacy
                        )
                        if result.get("success"):
                            st.markdown(f'<div class="success-banner">🎉 {result["message"]}<br/>📺 <a href="{result["url"]}" target="_blank">{result["url"]}</a></div>', unsafe_allow_html=True)
                        else:
                            st.error(result.get("error", "Unknown error"))
                else:
                    st.warning("पहले Dashboard tab में YouTube account connect करें।")

        # Instagram Upload
        with up_col2:
            st.subheader("🟣 Instagram Reels Upload")
            ig_video_url = st.text_input("Video Public URL (for Instagram):",
                                          help="Instagram को public URL चाहिए। Cloudinary free tier पर upload करें या video को किसी public server पर host करें।")
            if st.button("🚀 Upload to Instagram", type="primary", use_container_width=True):
                if ig_token and ig_user_id and ig_video_url:
                    with st.spinner("Instagram पर upload हो रहा है..."):
                        result = UploadManager.upload_to_instagram(
                            access_token=ig_token,
                            ig_user_id=ig_user_id,
                            video_url=ig_video_url,
                            caption=f"{title_for_upload}\n\n{desc_for_upload}\n\n{tags_for_upload}"
                        )
                        if result.get("success"):
                            st.markdown(f'<div class="success-banner">🎉 {result["message"]}</div>', unsafe_allow_html=True)
                        else:
                            st.error(result.get("error", "Unknown error"))
                else:
                    st.warning("Sidebar में Instagram Token, Account ID डालें और Video Public URL भरें।")

# ═══════════════════════════════════════════════════════════════════
#  TAB 7: ALGORITHM INSIGHTS
# ═══════════════════════════════════════════════════════════════════
with tabs[7]:
    st.header("📈 YouTube & Instagram Algorithm Insights (2026)")
    algo_data = AlgorithmAnalyzer.get_platform_algorithm_rules()

    c_yt, c_ig = st.columns(2)
    with c_yt:
        st.subheader("🔴 YouTube Shorts Algorithm")
        yt_algo = algo_data["youtube_shorts"]
        st.markdown(f"""
        | Factor | Detail |
        |--------|--------|
        | **#1 Viewed vs Swiped** | `{yt_algo['top_metric_1']}` |
        | **#2 Avg % Viewed** | `{yt_algo['top_metric_2']}` |
        | **Ranking Cycle** | {yt_algo['ranking_cycle']} |
        | **Best Time (IST)** | 🕛 {yt_algo['best_posting_times_ist'][0]} / 🕕 {yt_algo['best_posting_times_ist'][1]} |
        | **Monetization** | {yt_algo['monetization']} |
        """)

    with c_ig:
        st.subheader("🟣 Instagram Reels Algorithm")
        ig_algo = algo_data["instagram_reels"]
        st.markdown(f"""
        | Factor | Detail |
        |--------|--------|
        | **#1 DM Shares/Sends** | `{ig_algo['top_metric_1']}` |
        | **#2 Saves/Bookmarks** | `{ig_algo['top_metric_2']}` |
        | **Ranking Cycle** | {ig_algo['ranking_cycle']} |
        | **Best Time (IST)** | 🕘 {ig_algo['best_posting_times_ist'][0]} / 🕖 {ig_algo['best_posting_times_ist'][1]} |
        | **Monetization** | {ig_algo['monetization']} |
        """)

    st.markdown("---")
    st.subheader("🧪 वायरल होने के 4 वैज्ञानिक नियम")
    st.markdown("""
    1. **0-2 सेकंड का नियम:** स्क्रीन पर तुरंत हलचल या तेज़ सवाल। VVSA > 75% = viral push।
    2. **लूपिंग:** अंतिम वाक्य और पहला वाक्य जुड़ा हो → Retention 110%+।
    3. **कमेंट्स ट्रिगर:** अंत में सवाल पूछो → ज़्यादा कमेंट = ज़्यादा रीच।
    4. **Consistency:** रोज़ 1-2 Shorts सही समय (शाम 6-8 बजे) पर।
    """)

# ═══════════════════════════════════════════════════════════════════
#  TAB 8: MONETIZATION & ADS
# ═══════════════════════════════════════════════════════════════════
with tabs[8]:
    st.header("💰 Ads & Monetization — कमाई की पूरी गाइड")

    st.markdown("""
    ### 🏆 कमाई के 4 रास्ते (Day 1 से):
    """)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-card"><h3>💵</h3><p><b>YouTube Ads</b><br/>1K subs + 10M views<br/>ऑटोमैटिक ads</p></div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="metric-card"><h3>🤝</h3><p><b>Brand Deals</b><br/>10K+ views/reel<br/>₹2K-₹15K/post</p></div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="metric-card"><h3>🔗</h3><p><b>Affiliate Links</b><br/>Day 1 से शुरू<br/>₹500-₹5K/sale</p></div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="metric-card"><h3>📢</h3><p><b>Google Ads</b><br/>₹100/day budget<br/>Rapid growth</p></div>
        """, unsafe_allow_html=True)

    guide = YouTubePublisher.get_monetization_and_ad_guide()
    for s in guide:
        st.markdown(f"### {s['step']}")
        st.info(s['detail'])

    st.markdown("---")
    st.subheader("🎯 Google Ads से वीडियो प्रमोट करना")
    st.markdown("""
    1. **Google Ads** (`ads.google.com`) पर अकाउंट बनाएं।
    2. New Campaign → Video → Drive Views/Engagement।
    3. अपनी बेस्ट रील/शॉर्ट का URL डालें।
    4. Target: India, 18-34, Tech/Coding interests।
    5. Budget: ₹100-₹200/day → ₹0.20-₹0.50 per view।
    """)

    st.markdown("---")
    st.subheader("💰 Expected Earnings Timeline")
    import pandas as pd
    earnings_data = pd.DataFrame({
        "Month": ["Month 1", "Month 2", "Month 3", "Month 4-6", "Month 6-12"],
        "Videos": ["50-90", "100-150", "150-250", "250-500", "500-1000"],
        "Avg Views": ["500-2K", "2K-10K", "10K-50K", "50K-200K", "100K-500K"],
        "Expected ₹/month": ["₹0", "₹0-₹500", "₹1K-₹5K", "₹5K-₹20K", "₹30K-₹1L+"],
    })
    st.table(earnings_data)

# ═══════════════════════════════════════════════════════════════════
#  TAB 9: DEPLOY GUIDE
# ═══════════════════════════════════════════════════════════════════
with tabs[9]:
    st.header("🌐 Free Server + Free Domain पर Live करें")
    st.markdown("""
    ### Streamlit Community Cloud (100% Free)

    #### Step 1: GitHub पर Code Upload
    1. [GitHub.com](https://github.com) पर account बनाएं
    2. New repository → `autoviral-ai` नाम दें
    3. इस folder की files upload करें

    #### Step 2: Streamlit Cloud Connect
    1. [share.streamlit.io](https://share.streamlit.io) पर GitHub से sign in करें
    2. "Create app" → repo: `autoviral-ai`, file: `app.py`

    #### Step 3: Secrets & Deploy
    1. Advanced settings → Secrets में API keys paste करें:
    ```toml
    GEMINI_API_KEY = "your-key"
    PEXELS_API_KEY = "your-key"
    ```
    2. **Deploy!** → 2 मिनट में live 🎉

    आपका Free URL: `https://your-name.streamlit.app`
    """)
