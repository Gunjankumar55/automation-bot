from flask import Flask, request, jsonify
import subprocess
import os
import whisper

app = Flask(__name__)

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
        subprocess.run([
            "yt-dlp", "--cookies", "cookies.txt",
            "-f", "bestvideo+bestaudio/best",
            "-o", "input.%(ext)s", youtube_url
        ], check=True)

        input_file = next((f for f in ["input.mp4", "input.webm", "input.mkv"] if os.path.exists(f)), None)
        if not input_file:
            return jsonify({"error": "Downloaded file not found"}), 500

        print("🧠 Extracting audio...")
        audio_file = "audio.wav"
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            "-y", audio_file
        ], check=True)

        print("🧠 Transcribing using local Whisper...")
        model = whisper.load_model("base")  # You can also try "small", "medium", "large"
        result = model.transcribe(audio_file)

        srt_path = "subtitles.srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(result["segments"]):
                f.write(f"{i+1}\n")
                f.write(f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n")
                f.write(f"{seg['text'].strip()}\n\n")

        print("✅ Subtitles created")

        captioned_file = "captioned.mp4"
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vf", f"subtitles={srt_path}",
            "-c:a", "aac", "-c:v", "libx264", "-y", captioned_file
        ], check=True)

        output_file = "output.mp4"
        subprocess.run([
            "ffmpeg", "-stream_loop", "1", "-i", captioned_file,
            "-c", "copy", "-y", output_file
        ], check=True)

        print("✅ Video processed successfully")
        return jsonify({"status": "success", "output": output_file}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "stderr": e.stderr,
            "message": str(e)
        }), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
