# Downloader API
A free, open REST API that returns metadata and direct download links for media URLs. No files are stored or proxied — you get the CDN links directly.
Built on yt-dlp. Hosted free on Render.
## Base URL
[https://best-downloader.onrender.com](https://best-downloader.onrender.com)
> **Note:** Render's free tier spins down after inactivity. The first request after a period of no use may take 30–60 seconds to respond. Subsequent requests are fast.
> 
## Endpoints
### GET /info
Returns metadata and direct download links for a media URL.
#### Query Parameters

| Parameter | Required | Description |
| :--- | :--- | :--- |
| url | ✅ | The media URL to extract info from |

#### Example Request
```http
GET https://best-downloader.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
#### Example Response
```json
{
  "status": "success",
  "title": "Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster)",
  "uploader": "Rick Astley",
  "duration": 213,
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "extractor": "youtube",
  "formats": [
    {
      "format_id": "401",
      "quality": "2160p",
      "ext": "mp4",
      "vcodec": "av01.0.12M.08",
      "acodec": "none",
      "filesize": 240334643,
      "tbr": 9024.958,
      "url": "https://rr3---sn-....googlevideo.com/videoplayback?..."
    },
    {
      "format_id": "251",
      "quality": "medium",
      "ext": "webm",
      "vcodec": "none",
      "acodec": "opus",
      "filesize": 3433755,
      "tbr": 128.93,
      "url": "https://rr3---sn-....googlevideo.com/videoplayback?..."
    }
  ]
}
```
### Understanding the formats array
Each format is a separate stream. Common patterns:
 * **vcodec: "none"** → audio only stream
 * **acodec: "none"** → video only stream (no sound)
 * **Both present** → combined stream (ready to play as-is)
 * **Quality values:** 144p, 240p, 360p, 480p, 720p, 1080p, 1440p, 2160p
For a typical download, you want one video-only stream + one audio-only stream, then merge them with ffmpeg. Or just pick a combined 360p format if you want something simple.
⚠️ **Important: Links expire**
The direct URLs in the formats array are temporary CDN links. They expire within a few hours of being generated. Always call /info fresh when you need to download — **do not cache the URLs.**
### GET /health
Simple health check.
**Example Request**
```http
GET https://best-downloader.onrender.com/health 
```
**Example Response**
```json
{ "status": "ok" }
```
## Rate Limiting
**20 requests per hour per IP.** Exceeding this returns:
```json
{
  "error": "Rate limit exceeded. Max 20 requests per hour per IP."
}
```
## Error Responses

| Status | Meaning |
| :--- | :--- |
| **400** | Invalid URL (must start with http/https) |
| **422** | yt-dlp could not process this URL |
| **429** | Rate limit exceeded |
| **500** | Unexpected server error |

## Supported Sites
Anything **yt-dlp** supports — which is over 1,000 sites including YouTube, TikTok, Twitter/X, Reddit, Vimeo, SoundCloud, and many more.
## Usage Examples
### JavaScript (fetch)
```javascript
const response = await fetch(
  'https://best-downloader.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'
);
const data = await response.json(); 
// Get the best audio-only stream
const audio = data.formats.find(f => f.vcodec === 'none' && f.acodec !== 'none');
console.log(audio.url); 
```
### Python
```python
import requests 
r = requests.get(
    'https://best-downloader.onrender.com/info',
    params={'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
)
data = r.json() 
# Get all video formats sorted by quality
videos = [f for f in data['formats'] if f['acodec'] == 'none' and f['vcodec'] != 'none']
print(videos) 
```
### cURL
```bash
curl "https://best-downloader.onrender.com/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
## Self Hosting
```bash
git clone https://github.com/Izaz80/BestDownloader
cd BestDownloader
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 
```
*Requires Python 3.11+ and ffmpeg installed on the system.*
## License
**MIT** — do whatever you want with it.
## Disclaimer
This API is a resolver — it returns links that already exist publicly on CDN servers. Users are responsible for complying with the terms of service of any platform they query. No content is stored on this server.
