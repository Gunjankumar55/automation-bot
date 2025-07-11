#!/bin/bash

echo "Starting FFmpeg job..."
ffmpeg -i input.mp4 -vf "scale=720:-1" output.mp4
echo "Done!"
