import streamlit as st
import os
import base64
from supabase import create_client
from dl import run_downloader

# --- PAGE CONFIG ---
st.set_page_config(page_title="UltraDL Pro", page_icon="🚀", layout="centered")

# --- BOOTSTRAP-INSPIRED CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main .block-container { padding-top: 8rem; }
    
    /* The One-Click Download Button Styling */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff;
        border-radius: 4px;
        height: 3.5rem;
        font-weight: bold;
        width: 100%;
        font-size: 1.2rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #cccccc !important;
    }
    
    .stTextInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        height: 3.1rem;
    }
    h1, .stCaption { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTO-DOWNLOAD HELPER ---
def trigger_auto_download(file_path):
    """Injects JS to trigger an immediate browser download"""
    with open(file_path, "rb") as f:
        data = f.read()
    
    b64 = base64.b64encode(data).decode()
    file_name = os.path.basename(file_path)
    
    # JavaScript to create a ghost link and click it automatically
    dl_script = f"""
        <script>
            var a = document.createElement('a');
            a.href = 'data:application/octet-stream;base64,{b64}';
            a.download = '{file_name}';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        </script>
    """
    st.components.v1.html(dl_script, height=0)

# --- UI BODY ---
st.title("🚀 UltraDL Pro")
st.caption("Direct Media Engine | One-Click Delivery")

col1, col2 = st.columns([1, 3])
with col1:
    mode_map = {
        "🎥 Video": "default",
        "🎵 Audio": "aud",
        "📂 Playlist": "pl",
        "🖼️ Images": "thum"
    }
    selected_label = st.selectbox("", list(mode_map.keys()), label_visibility="collapsed")
    mode = mode_map[selected_label]

with col2:
    url_input = st.text_input("", placeholder="Paste link here...", label_visibility="collapsed")

# Changed label to 'DOWNLOAD' as requested
if st.button("DOWNLOAD"):
    if not url_input:
        st.error("Please provide a URL.")
    else:
        with st.status("⚡ Processing...", expanded=True) as status:
            # 1. Run the downloader
            file_path = run_downloader(url_input, mode)
            
            if file_path and os.path.exists(file_path):
                status.update(label="✅ Success! Starting Download...", state="complete")
                
                # 2. Trigger the "One-Click" JS injection
                trigger_auto_download(file_path)
                
                # 3. Clean up server storage
                os.remove(file_path)
            else:
                status.update(label="❌ Error", state="error")
