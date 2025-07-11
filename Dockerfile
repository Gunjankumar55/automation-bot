FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp

# Set working directory
WORKDIR /app

# Copy Flask app
COPY main.py .

# Expose port for Railway
EXPOSE 5000

# Start Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
