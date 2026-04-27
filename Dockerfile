FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY lib/ lib/
COPY gopro-download.py gopro-organize.py gopro-sync.py ./

# Media output is mounted at /data
VOLUME ["/data"]

# Default to running the full sync (download + organize)
CMD ["python", "gopro-sync.py"]
