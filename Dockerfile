FROM python:3.11-slim

# Install FFmpeg
RUN apt update && apt install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Run the script
ENTRYPOINT ["bash", "entrypoint.sh"]
