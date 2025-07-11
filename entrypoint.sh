#!/bin/bash

# Auto-processing script (example: re-encode input.mp4 to output.mp4)
echo "Running FFmpeg on input.mp4..."

if [ ! -f /videos/input.mp4 ]; then
  echo "❌ input.mp4 not found in /videos folder!"
  exit 1
fi

ffmpeg -i /videos/input.mp4 -vf "scale=720:-1" /videos/output.mp4

echo "✅ Processing complete. File saved to /videos/output.mp4"
