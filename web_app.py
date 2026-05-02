import streamlit as st
import os
from supabase import create_client
from dl import run_downloader

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="UltraDL Pro",
    page_icon="🚀",
    layout="centered"
)

# --- BOOTSTRAP-INSPIRED CUSTOM CSS ---
# This mimics the high-contrast dark theme and the specific button/input styling
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Centralized Container Padding */
    .main .block-container { padding-top: 10rem; }
    
    /* Mimicking the "black-background white" search button */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff;
        border-radius: 0px 5px 5px 0px;
        height: 3.1rem;
        font-weight: bold;
        width: 100%;
    }
    
    /* Input field styling to match Bootstrap 3.3.6 defaults */
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 5px 0px 0px 5px;
        height: 3.1rem;
    }
    
    /* Adjusting selectbox to look like the Category/Engine dropdowns */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 5px;
        background-color: #333333;
    }
    
    h1 { text-align: center; font-family: sans-serif; font-weight: bold; }
    .stCaption { text-align: center; color: #aaaaaa; }
    </style>
    """, unsafe_allow_html=True)

# --- BACKEND LOGIC ---
SUPA_URL = os.environ.get("SUPABASE_URL", "")
SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

def silent_log(url, mode):
    if SUPA_URL and SUPA_KEY:
        try:
            supabase = create_client(SUPA_URL, SUPA_KEY)
            supabase.table("download_logs").insert({"video_url": url, "download_mode": mode}).execute()
        except: pass

# --- UI HEADER ---
st.title("🚀 UltraDL Pro")
st.caption("Find direct download links for about anything. Take advantage of powerful engines.") # Inspired by description

# --- UI BODY: THE SEARCH GROUP ---
# The original UI uses a grid system (col-lg-8) to center the search bar
col1, col2 = st.columns([1, 4])

with col1:
    # Mimics the "Category" dropdown (Software, Movies, Music, etc.)
    mode_map = {
        "🎥 Video": "default",
        "🎬 No Thumb": "nothum",
        "🖼️ Thumb Only": "thum",
        "🎵 Audio Only": "aud",
        "📂 Playlist": "pl",
        "🎞️ Pl No Thumb": "pl nothum",
        "📸 Pl Thumb": "pl thum",
        "🎧 Pl Audio": "pl aud"
    }
    selected_label = st.selectbox("", list(mode_map.keys()), label_visibility="collapsed")
    mode = mode_map[selected_label]

with col2:
    # Mimics the main search input field
    url_input = st.text_input("", placeholder="Paste link e.g. https://youtube.com/watch?v=...", label_visibility="collapsed")

# The search button centered below, mimicking the "startSearch()" trigger
if st.button("INITIALIZE ENGINE"):
    if not url_input:
        st.warning("⚠️ Please provide a URL.")
    else:
        silent_log(url_input, mode)
        
        with st.status("⚡ Processing...", expanded=False) as status:
            file_path = run_downloader(url_input, mode)
            
            if file_path and os.path.exists(file_path):
                status.update(label="✅ Ready for Device Transfer!", state="complete")
                
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"💾 SAVE {os.path.basename(file_path).upper()}",
                        data=f.read(),
                        file_name=os.path.basename(file_path),
                        mime="application/octet-stream",
                        use_container_width=True
                    )
                os.remove(file_path)
            else:
                status.update(label="❌ Engine Error", state="error")

# --- FOOTER ---
st.markdown("<br><br><center><small>Powered by yt-dlp | Bootstrap Dark Aesthetic</small></center>", unsafe_allow_html=True)
