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

if st.button("Start Download"):
    if url_input:
        silent_log(url_input, mode) 
        with st.spinner("🚀 Downloading to server..."):
            # 1. Run the downloader and get the file path
            file_path = run_downloader(url_input, mode.lower())
            
            if file_path and os.path.exists(file_path):
                st.success("✅ Processed! Click below to save to your device.")
                
                # 2. Open the file in binary mode
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                    
                    # 3. Create the actual browser download button
                    st.download_button(
                        label="💾 Download File to Device",
                        data=file_data,
                        file_name=file_name,
                        mime="application/octet-stream"
                    )
                
                # 4. Optional: Clean up the server storage after reading it into memory
                os.remove(file_path)
            else:
                st.error("Failed to find the downloaded file. Try a different link.")
