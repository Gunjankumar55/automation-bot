FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg curl unzip

# Copy script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create folder to store videos (this will be handled by Railway volumes later)
RUN mkdir -p /videos

WORKDIR /videos

ENTRYPOINT ["/entrypoint.sh"]
