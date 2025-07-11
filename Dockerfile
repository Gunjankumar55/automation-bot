FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libsndfile1 curl && \
    pip install --no-cache-dir torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir flask yt-dlp openai-whisper && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Make entrypoint executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
