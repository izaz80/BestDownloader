from fastapi import FastAPI
import yt_dlp
import uvicorn

app = FastAPI()

@app.get("/test")
def test():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 15,
        'noplaylist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "status": "success",
                "title": info.get("title"),
                "formats_count": len(info.get("formats", []))
            }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
