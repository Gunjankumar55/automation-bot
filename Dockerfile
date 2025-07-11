FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask yt-dlp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files (main.py, cookies.txt, etc.)
COPY . .

# Set Flask app
ENV FLASK_APP=main.py

# Expose port (for Railway)
EXPOSE 5000

# Start Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
