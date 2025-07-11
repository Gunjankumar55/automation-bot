FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    pip install --no-cache-dir flask yt-dlp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all source code and support files
COPY . .

# Convert entrypoint.sh to LF (safe for Windows users via Docker) and make it executable
RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh

# Expose port (Railway auto-maps)
EXPOSE 5000

# Run the app
ENTRYPOINT ["./entrypoint.sh"]
