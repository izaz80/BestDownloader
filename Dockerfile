FROM python:3.11-slim

# Install ALL system dependencies in one layer
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all needed files
COPY requirements.txt .
COPY web_app.py .
COPY dl.py .
COPY test_api.py .
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
