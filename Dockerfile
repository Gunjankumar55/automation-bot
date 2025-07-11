FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask yt-dlp && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files (main.py, etc.)
COPY . .

# Tell Flask which app to run
ENV FLASK_APP=main.py

# Expose port (Railway maps this automatically)
EXPOSE 5000

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
