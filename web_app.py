import streamlit as st
import os
from supabase import create_client
from dl import run_downloader

# --- 2026 ULTRA-UI CONFIG ---
st.set_page_config(page_title="UltraDL Pro", page_icon="⚡", layout="centered")

# --- HIGH-END CSS OVERHAUL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
        background-color: #000000;
    }

    /* Force Two Rows on All Devices */
    .custom-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        margin-bottom: 20px;
    }

    /* Input Styling */
    .stTextInput input {
        background-color: #111 !important;
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        padding: 25px !important;
        font-size: 18px !important;
        color: #fff !important;
    }
    
    .stTextInput input:focus {
        border-color: #FF4B4B !important;
    }

    /* Selectbox (Mode) Styling */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #111 !important;
        border: 2px solid #333 !important;
        border-radius: 12px !important;
        height: 50px !important;
    }

    /* The Massive 'One-Click' Action Button */
    .stButton button, .stDownloadButton button {
        width: 100% !important;
        background: #FF4B4B !important;
        border: none !important;
        padding: 30px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.4) !important;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 75, 75, 0.6) !important;
    }

    /* Status Box Styling */
    div[data-testid="stStatusWidget"] {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
st.markdown("<h1 style='text-align: center; font-weight: 800; letter-spacing: -1px;'>UltraDL Pro</h1>", unsafe_allow_html=True)

# Input Section (Two Fixed Rows)
url_input = st.text_input("Link", placeholder="Paste URL and click Fetch", label_visibility="collapsed")

mode_map = {
    "🎬 High-Res Video": "default",
    "🎵 MP3 Audio": "aud",
    "📸 Thumbnail Only": "thum",
    "📂 Full Playlist": "pl"
}
mode_label = st.selectbox("Mode", list(mode_map.keys()), label_visibility="collapsed")
mode = mode_map[mode_label]

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# THE TRIGGER
# Since we want to avoid 'Enter', we use a big "Fetch" button as the primary action.
if st.button("🚀 FETCH MEDIA"):
    if not url_input:
        st.error("Missing URL")
    else:
        with st.status("⚡ Processing Engine...", expanded=False) as status:
            # Download Logic
            file_path = run_downloader(url_input, mode)
            
            if file_path and os.path.exists(file_path):
                status.update(label="✅ Ready", state="complete")
                
                with open(file_path, "rb") as f:
                    # Instant Reveal of the Save Button
                    st.download_button(
                        label="⬇️ SAVE TO DEVICE",
                        data=f.read(),
                        file_name=os.path.basename(file_path),
                        mime="application/octet-stream",
                        use_container_width=True
                    )
                os.remove(file_path)
            else:
                status.update(label="❌ Error", state="error")
                st.error("Link expired or unsupported.")

st.markdown("<center style='opacity: 0.5; margin-top: 50px;'><small>v2.0.26 | No Tracking | Pure Speed</small></center>", unsafe_allow_html=True)
