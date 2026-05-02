import streamlit as st
import os
import time
from supabase import create_client
from dl import run_downloader

# --- 2026 ULTRA-UI CONFIG ---
st.set_page_config(page_title="UltraDL Pro", page_icon="⚡", layout="centered")

# Injection of High-End CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2e, #000000);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Glassmorphism Card */
    div[data-testid="stVerticalBlock"] > div:has(input) {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Input Styling */
    .stTextInput input {
        background-color: rgba(0,0,0,0.5) !important;
        border: 1px solid #444 !important;
        color: #fff !important;
        font-size: 1.2rem !important;
        height: 60px !important;
    }

    /* Primary Button Transformation */
    .stDownloadButton button {
        background: linear-gradient(90deg, #FF4B4B 0%, #ff8080 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        height: 3.5em !important;
        transition: all 0.3s ease;
        box-shadow: 0px 10px 20px rgba(255, 75, 75, 0.3);
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 15px 25px rgba(255, 75, 75, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
SUPA_URL = os.environ.get("SUPABASE_URL", "")
SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

def silent_log(url, mode):
    if SUPA_URL and SUPA_KEY:
        try:
            supabase = create_client(SUPA_URL, SUPA_KEY)
            supabase.table("download_logs").insert({"video_url": url, "download_mode": mode}).execute()
        except: pass

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: white;'>⚡ UltraDL Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Paste. Download. Done.</p>", unsafe_allow_html=True)

# --- APP CORE ---
# We use columns to put the Mode and Input on the same visual plane
col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input("", placeholder="https://youtube.com/watch?v=...", label_visibility="collapsed")

with col2:
    mode_map = {
        "🎬 Video": "default",
        "📸 Thumb": "thum",
        "🎵 Audio": "aud",
        "📂 Playlist": "pl"
    }
    selected_label = st.selectbox("", list(mode_map.keys()), label_visibility="collapsed")
    mode = mode_map[selected_label]

# --- THE AUTO-ENGINE ---
if url_input:
    # Triggered immediately when URL is detected
    silent_log(url_input, mode)
    
    with st.status("🚀 Fetching Media...", expanded=False) as status:
        file_path = run_downloader(url_input, mode)
        
        if file_path and os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            
            status.update(label="✅ Ready!", state="complete")
            
            # The Magic: The Save button appears automatically
            st.download_button(
                label=f"⬇️ SAVE {file_name.upper()}",
                data=file_bytes,
                file_name=file_name,
                mime="application/octet-stream",
                use_container_width=True,
                on_click=lambda: os.remove(file_path) # Cleanup on click
            )
        else:
            status.update(label="❌ Failed", state="error")
            st.error("Engine couldn't grab that link. Try a different format.")

# --- FOOTER ---
st.markdown("<div style='margin-top: 100px; opacity: 0.3; text-align: center; font-size: 0.8rem;'>High-Fidelity Engine v2.6.4</div>", unsafe_allow_html=True)
