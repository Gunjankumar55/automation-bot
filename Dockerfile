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
    numpy \
    flask \
    yt-dlp \
    openai

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Fix entrypoint permissions
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose port
EXPOSE 5000

# Run app
ENTRYPOINT ["./entrypoint.sh"]
