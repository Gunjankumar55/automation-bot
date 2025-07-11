FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    curl \
    fontconfig \
    gcc \
    g++ \
    python3-dev \
    build-essential \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Pin NumPy to compatible version BEFORE torch/whisper
RUN pip install --no-cache-dir numpy==1.26.4

# Install other Python dependencies
RUN pip install --no-cache-dir \
    flask \
    yt-dlp

# Install PyTorch CPU-only versions (use correct index)
RUN pip install --no-cache-dir \
    torch==2.2.2 \
    torchvision==0.17.2 \
    torchaudio==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu

# Install Whisper
RUN pip install --no-cache-dir openai-whisper

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Fix line endings + permission on entrypoint.sh
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose Flask app port
EXPOSE 5000

# Run Flask app via entrypoint
ENTRYPOINT ["./entrypoint.sh"]
