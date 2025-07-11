# Use lightweight FFmpeg image
FROM jrottenberg/ffmpeg:4.4-ubuntu

# Set working directory
WORKDIR /app

# Copy script into container
COPY entrypoint.sh /app/entrypoint.sh

# Make script executable
RUN chmod +x /app/entrypoint.sh

# Create and mount videos directory
VOLUME ["/videos"]

# Run the script automatically
CMD ["/app/entrypoint.sh"]
