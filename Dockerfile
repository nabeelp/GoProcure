FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY lib/ lib/
COPY gopro-download.py gopro-organize.py gopro-sync.py ./

# Media output is mounted at /data
VOLUME ["/data"]

# Default to running the full sync (download + organize)
CMD ["python", "gopro-sync.py"]
