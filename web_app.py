import streamlit as st
import os
from supabase import create_client
from dl import run_downloader

# Database Config (Silent)
SUPA_URL = os.environ.get("SUPABASE_URL", "")
SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

def silent_log(url, mode):
    if SUPA_URL and SUPA_KEY:
        try:
            supabase = create_client(SUPA_URL, SUPA_KEY)
            supabase.table("download_logs").insert({"video_url": url, "download_mode": mode}).execute()
        except: pass # Fails silently so user never knows

st.title("🚀 Media Downloader")
url_input = st.text_input("Paste Link:")
mode = st.selectbox("Quality:", ["Default", "Audio Only", "Playlist"])

if st.button("Download"):
    if url_input:
        silent_log(url_input, mode) # Happens in background
        with st.spinner("Fetching best quality..."):
            run_downloader(url_input, mode.lower())
            st.success("Download processed on server!")
            # Note: In Step 6 we'll add the button to actually save to phone
