#!/bin/sh

mkdir -p /video
ffmpeg -i /video/input.mp4 -vf "scale=720:-2" /video/output.mp4
