import os
import subprocess
import sys
import yt_dlp

# --- CONFIGURATION ---
FINAL_DIR = "./downloads"
os.makedirs(FINAL_DIR, exist_ok=True)
COOKIES_PATH = os.path.expanduser("~/cookies.txt")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def run_downloader(url, mode="default"):
    print(f"🚀 Mode: {mode} (Ultra-Quality Enabled)")

    # Base Options (Equivalent to your FLAGS)
    ydl_opts = {
        'nocheckcertificate': True,
        'user_agent': USER_AGENT,
        'cookiefile': COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        'writemetadata': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(FINAL_DIR, "%(uploader)s_%(id)s_%(playlist_index)s.%(ext)s"),
        'format': 'bv+ba/b',
        'merge_output_format': 'mkv',
        'javascript_delay': 5, # Similar to quickjs runtime behavior
    }

    # --- LOGIC (Case/Switch equivalent) ---
    if mode == "nothum":
        ydl_opts['writethumbnail'] = False
    elif mode == "thum":
        ydl_opts.update({'writethumbnail': True, 'skip_download': True})
    elif mode == "aud":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '0'}],
        })
    elif mode == "pl":
        ydl_opts.update({'noplaylist': False, 'writethumbnail': True})
    elif mode == "pl nothum":
        ydl_opts.update({'noplaylist': False, 'writethumbnail': False})
    elif mode == "pl thum":
        ydl_opts.update({'noplaylist': False, 'writethumbnail': True, 'skip_download': True})
    elif mode == "pl aud":
        ydl_opts.update({
            'noplaylist': False,
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '0'}],
        })
    else: # default
        ydl_opts.update({'writethumbnail': True, 'noplaylist': True})

    # --- EXECUTION ---
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        error_msg = str(e)
        print(f"Error caught: {error_msg}")

        # --- GALLERY-DL FALLBACK ---
        if "No video formats found" in error_msg or "Unsupported URL" in error_msg:
            print("📸 Image-only post detected. Switching to gallery-dl...")
            g_cmd = [
                "gallery-dl",
                "--cookies", COOKIES_PATH,
                "-o", f"base-directory={FINAL_DIR}",
                "-o", "module.instagram.posts.fullsize=true",
                url
            ]
            subprocess.run(g_cmd)

    # --- CLEANUP ---
    # Python makes moving files and deleting empty folders very fast
    for root, dirs, files in os.walk(FINAL_DIR, topdown=False):
        for name in files:
            source = os.path.join(root, name)
            target = os.path.join(FINAL_DIR, name)
            if source != target:
                os.replace(source, target)
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    print(f"✅ Done! Files are in {FINAL_DIR}")

if __name__ == "__main__":
    # Handle command line args like your bash script
    if len(sys.argv) < 2:
        print("Usage: python dl.py <URL> <MODE(optional)>")
    else:
        u = sys.argv[1]
        m = sys.argv[2] if len(sys.argv) > 2 else "default"
        run_downloader(u, m)
