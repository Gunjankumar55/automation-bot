from flask import Flask, request, jsonify
import numpy as np
import subprocess
import os
import openai
import tempfile

app = Flask(__name__)

# Set your OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/upload-cookies', methods=['POST'])
def upload_cookies():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file.save('/app/cookies.txt')
    return jsonify({"status": "cookies uploaded"}), 200

@app.route('/process', methods=['POST'])
def process_video():
    data = request.get_json()
    if not data or 'videoId' not in data:
        return jsonify({"error": "Missing 'videoId'"}), 400

    video_id = data['videoId']
    title = data.get('title', 'Untitled')
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        print(f"▶ Downloading: {youtube_url}")

        # Step 1: Download video
        download_cmd = [
            "yt-dlp", "--cookies", "cookies.txt",
            "-f", "bestvideo+bestaudio/best",
            "-o", "input.%(ext)s", youtube_url
        ]
        subprocess.run(download_cmd, check=True)

        # Step 2: Find downloaded file
        input_file = next((f for f in ["input.mp4", "input.webm", "input.mkv"] if os.path.exists(f)), None)
        if not input_file:
            return jsonify({"error": "Downloaded file not found"}), 500

        print("🧠 Extracting audio for OpenAI Whisper API...")

        # Step 3: Extract audio
        audio_file = "audio.mp3"
        subprocess.run([
            "ffmpeg", "-i", input_file, "-vn", "-acodec", "libmp3lame", "-y", audio_file
        ], check=True)

        print("🎙 Transcribing via OpenAI Whisper API...")
        with open(audio_file, "rb") as audio:
            transcript = openai.Audio.transcribe("whisper-1", audio)

        # Step 4: Save .srt subtitles
        srt_path = "subtitles.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            segments = transcript.get("segments", [])
            if not segments:  # fallback if segments not present
                text = transcript.get("text", "")
                f.write("1\n00:00:00,000 --> 00:00:10,000\n" + text + "\n")
            else:
                for i, segment in enumerate(segments):
                    start = format_time(segment["start"])
                    end = format_time(segment["end"])
                    text = segment["text"].strip()
                    f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")

        print("✅ Subtitles saved to:", srt_path)

        # Step 5: Burn subtitles
        captioned_file = "captioned.mp4"
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vf", f"subtitles={srt_path}",
            "-c:a", "aac", "-c:v", "libx264", "-y", captioned_file
        ], check=True)

        # Step 6: Loop video
        output_file = "output.mp4"
        subprocess.run([
            "ffmpeg", "-stream_loop", "1", "-i", captioned_file,
            "-c", "copy", "-y", output_file
        ], check=True)

        return jsonify({"status": "success", "output": output_file}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "stderr": e.stderr,
            "message": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
