import sys
import os
from pytube import YouTube
import subprocess

def download_video(url, filename="input.mp4"):
    print(f"Downloading {url}...")
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download(filename=filename)
    print(f"Downloaded as {filename}")
    return filename

def clip_video(input_file="input.mp4", output_file="output.mp4"):
    print("Clipping video with FFmpeg...")
    # First 30 seconds
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file,
        "-ss", "00:00:00", "-t", "00:00:30",
        "-vf", "scale=1080:1920",  # optional portrait mode
        output_file
    ])
    print(f"Output saved as {output_file}")

if __name__ == "__main__":
    url = sys.argv[1]
    input_file = download_video(url)
    clip_video(input_file)
