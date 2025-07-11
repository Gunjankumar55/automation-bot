FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask yt-dlp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything including cookies
COPY . .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose Railway port
EXPOSE 5000

# Run the app
ENTRYPOINT ["./entrypoint.sh"]
