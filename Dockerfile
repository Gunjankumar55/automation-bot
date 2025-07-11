FROM python:3.10-slim

# Install system dependencies for ffmpeg, whisper, numpy, etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libsndfile1 \
        curl \
        fontconfig \
        gcc \
        g++ \
        python3-dev \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python env vars for reliable builds
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install compatible Python packages
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    flask \
    yt-dlp && \
    pip install --no-cache-dir \
    torch==2.2.2 \
    torchvision==0.17.2 \
    torchaudio==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir openai-whisper

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Ensure entrypoint.sh is Unix-formatted and executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose Flask port
EXPOSE 5000

# Run the app
ENTRYPOINT ["./entrypoint.sh"]
