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

# --- CUSTOM CSS FOR 2026 UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SILENT TRACKING ---
SUPA_URL = os.environ.get("SUPABASE_URL", "")
SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

def silent_log(url, mode):
    if SUPA_URL and SUPA_KEY:
        try:
            supabase = create_client(SUPA_URL, SUPA_KEY)
            supabase.table("download_logs").insert({"video_url": url, "download_mode": mode}).execute()
        except:
            pass

# --- UI HEADER ---
st.title("🚀 UltraDL Pro")
st.caption("2026 Browser-First Media Engine | High-Fidelity Downloads")

# --- UI BODY ---
with st.container():
    url_input = st.text_input("", placeholder="Paste your link here (YouTube, Instagram, etc.)")
    
    # Mapping your dl.py modes to user-friendly labels
    mode_map = {
        "Video + Thumbnail": "default",
        "Video (No Thumbnail)": "nothum",
        "Thumbnail Only": "thum",
        "Audio Only (MP3)": "aud",
        "Full Playlist": "pl",
        "Playlist (No Thumbnails)": "pl nothum",
        "Playlist Thumbnails": "pl thum",
        "Playlist Audio Only": "pl aud"
    }
    
    selected_label = st.selectbox("Download Quality & Mode", list(mode_map.keys()))
    mode = mode_map[selected_label]

st.divider()

if st.button("Initialize Engine"):
    if not url_input:
        st.warning("⚠️ Please provide a URL.")
    else:
        # Step 1: Silent Log
        silent_log(url_input, mode)
        
        # Step 2: Download on Server
        with st.status("⚡ Processing...", expanded=True) as status:
            st.write("Initializing yt-dlp/gallery-dl...")
            file_path = run_downloader(url_input, mode)
            
            if file_path and os.path.exists(file_path):
                status.update(label="✅ Ready for Device Transfer!", state="complete", expanded=False)
                
                # Step 3: Serve to User
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    file_name = os.path.basename(file_path)
                    
                    st.download_button(
                        label=f"💾 Save {file_name}",
                        data=file_bytes,
                        file_name=file_name,
                        mime="application/octet-stream",
                        use_container_width=True
                    )
                
                # Step 4: Server Cleanup
                os.remove(file_path)
            else:
                status.update(label="❌ Engine Error", state="error")
                st.error("The file could not be generated. Check the link or try another mode.")

# --- FOOTER ---
st.markdown("<br><center><small>Powered by yt-dlp & gallery-dl | Ephemeral Cloud Storage</small></center>", unsafe_allow_html=True)
