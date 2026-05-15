# Use a lightweight Python image
FROM python:3.11-slim

# 1. Install system dependencies (ffmpeg is required for yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a working directory inside the container
WORKDIR /app

# 3. Copy ONLY the necessary files (This prevents leaking other scripts)
COPY requirements.txt .
COPY web_app.py .
COPY dl.py .
# If you have a cookies file, we will handle it via 'Secrets' later,
# do NOT copy it directly into the image if you want to be safe.

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the port Streamlit runs on
EXPOSE 8501

# Install supervisor to run two processes
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY test_api.py .

EXPOSE 8501
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
