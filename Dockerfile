FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    curl \
    fontconfig \
    gcc \
    g++ \
    python3-dev \
    build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install --no-cache-dir \
    flask \
    yt-dlp \
    openai==1.14.2 \
    numpy

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Fix entrypoint permissions (if needed)
RUN chmod +x entrypoint.sh || true

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "main.py"]
