FROM python:3.10-slim

# Install system dependencies & tools required for numpy and audio processing
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

# Install Python dependencies
# Install standard PyPI packages first
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    flask \
    yt-dlp

# Install torch packages from PyTorch CPU index
RUN pip install --no-cache-dir \
    torch==2.2.2 \
    torchvision==0.17.2 \
    torchaudio==2.2.2 \
    --index-url https://download.pytorch.org/whl/cpu

# Install Whisper
RUN pip install --no-cache-dir openai-whisper

# Set working directory
WORKDIR /app

# Copy everything into container (main.py, entrypoint.sh, cookies.txt, etc.)
COPY . .

# Ensure entrypoint.sh has Unix line endings and is executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose port (Railway automatically maps this)
EXPOSE 5000

# Launch the Flask app using entrypoint
ENTRYPOINT ["./entrypoint.sh"]
