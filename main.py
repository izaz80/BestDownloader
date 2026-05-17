from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
import yt_dlp
import time
from collections import defaultdict

app = FastAPI(
    title="MediaInfo API",
    description="Returns metadata and direct download links for media URLs. No files are stored or proxied.",
    version="1.0.0"
)

# --- Simple in-memory rate limiter ---
# Stores {ip: [timestamp, timestamp, ...]}
request_log = defaultdict(list)
RATE_LIMIT = 200       # max requests
RATE_WINDOW = 60 * 60 # per hour

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - RATE_WINDOW
    # Keep only requests within the window
    request_log[ip] = [t for t in request_log[ip] if t > window_start]
    if len(request_log[ip]) >= RATE_LIMIT:
        return True
    request_log[ip].append(now)
    return False

# --- Helpers ---
def clean_formats(formats: list) -> list:
    cleaned = []
    for f in formats:
        # Skip formats with no URL
        if not f.get("url"):
            continue
        cleaned.append({
            "format_id": f.get("format_id"),
            "quality": f.get("format_note") or f.get("resolution") or "unknown",
            "ext": f.get("ext"),
            "vcodec": f.get("vcodec"),
            "acodec": f.get("acodec"),
            "filesize": f.get("filesize") or f.get("filesize_approx"),
            "tbr": f.get("tbr"),
            "url": f.get("url"),
        })
    return cleaned

# --- Routes ---
@app.get("/")
def root():
    return {
        "name": "MediaInfo API",
        "version": "1.0.0",
        "endpoints": {
            "/info": "GET ?url=<media_url> — returns metadata and direct download links",
            "/health": "GET — service health check"
        },
        "note": "This API returns direct links from source CDNs. No files are stored on this server."
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def get_info(request: Request, url: str = Query(..., description="Media URL to extract info from")):
    # Rate limiting
    client_ip = request.client.host
    if is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Max 20 requests per hour per IP."}
        )

    if not url.startswith("http"):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid URL. Must start with http:// or https://"}
        )

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 20,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "status": "success",
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url"),
            "extractor": info.get("extractor"),
            "formats": clean_formats(info.get("formats", [])),
        }

    except yt_dlp.utils.DownloadError as e:
        return JSONResponse(
            status_code=422,
            content={"error": "yt-dlp could not process this URL", "detail": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Unexpected error", "detail": str(e)}
        )
