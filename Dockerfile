FROM python:3.10-slim

# Install ffmpeg and yt-dlp
RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install flask yt-dlp

# Create working directory
WORKDIR /app

# Copy files
COPY main.py .

# Set environment variable for Flask
ENV FLASK_APP=main.py

# Expose port for Railway
EXPOSE 5000

# Start the server
CMD ["flask", "run", "--host=0.0.0.0", "--port=${PORT}"]
