import streamlit as st
import os
import time
from supabase import create_client
from dl import run_downloader

# --- PAGE CONFIG ---
st.set_page_config(page_title="UltraDL Pro", page_icon="⚡", layout="centered")

# --- 2026 NEON GLASSMORPHISM UI ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .main { background: radial-gradient(circle at top left, #1a1a2e, #0f0f1b); color: #ffffff; }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-size: 1.1rem !important;
    }

    /* Modern Selectbox */
    .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
    }

    /* THE ONE-CLICK BUTTON */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        border: none;
        color: white;
        padding: 20px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
def silent_log(url, mode):
    SUPA_URL = os.environ.get("SUPABASE_URL", "")
    SUPA_KEY = os.environ.get("SUPABASE_KEY", "")
    if SUPA_URL and SUPA_KEY:
        try:
            supabase = create_client(SUPA_URL, SUPA_KEY)
            supabase.table("download_logs").insert({"video_url": url, "download_mode": mode}).execute()
        except: pass

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>⚡ UltraDL Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 0.9rem;'>Premium Media Extraction Engine</p>", unsafe_allow_html=True)
st.write("---")

# --- UI BODY ---
col1, col2 = st.columns([2, 1])

with col1:
    url_input = st.text_input("Source URL", placeholder="Paste link here...", label_visibility="collapsed")

with col2:
    mode_map = {
        "🎬 Video + Meta": "default",
        "🎥 Raw Video": "nothum",
        "🖼️ Thumbnail": "thum",
        "🎵 MP3 Audio": "aud",
        "📂 Playlist": "pl"
    }
    selected_label = st.selectbox("Mode", list(mode_map.keys()), label_visibility="collapsed")
    mode = mode_map[selected_label]

# Action Space
main_btn_placeholder = st.empty()

if main_btn_placeholder.button("⚡ GRAB MEDIA"):
    if not url_input:
        st.toast("⚠️ Drop a link first!", icon="🔥")
    else:
        silent_log(url_input, mode)
        
        with st.status("🚀 Teleporting media...", expanded=False) as status:
            file_path = run_downloader(url_input, mode)
            
            if file_path and os.path.exists(file_path):
                status.update(label="✅ Ready!", state="complete")
                
                # We show the final Save button immediately in place of the old one
                with open(file_path, "rb") as f:
                    file_name = os.path.basename(file_path)
                    st.download_button(
                        label=f"⬇️ SAVE {file_name.upper()}",
                        data=f.read(),
                        file_name=file_name,
                        mime="application/octet-stream",
                        use_container_width=True,
                        key="final_dl"
                    )
                os.remove(file_path)
            else:
                status.update(label="❌ Failed", state="error")
                st.error("Link invalid or server busy.")

# --- FOOTER ---
st.markdown("<div style='margin-top: 100px; text-align: center; opacity: 0.5; font-size: 0.7rem;'>2026 ULTRA SERIES | DISCRETE CLOUD PROCESSING</div>", unsafe_allow_html=True)
