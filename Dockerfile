FROM python:3.10-slim

# Install system dependencies and build tools for numpy to compile
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

# Install Python libraries — install numpy FIRST
RUN pip install --no-cache-dir \
    numpy \
    flask \
    yt-dlp \
    torch==2.2.2 \
    torchvision==0.17.2 \
    torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir openai-whisper

# Set working directory
WORKDIR /app

# Copy all files including main.py, entrypoint.sh, cookies.txt
COPY . .

# Make entrypoint script executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose port
EXPOSE 5000

# Start backend
ENTRYPOINT ["./entrypoint.sh"]
