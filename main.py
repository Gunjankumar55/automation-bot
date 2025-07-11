from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/upload-cookies', methods=['POST'])
def upload_cookies():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file.save('/app/cookies.txt')  # Save over existing
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

        # Download using yt-dlp with cookies
        download_cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bestvideo+bestaudio/best",
            "-o", "input.%(ext)s",
            youtube_url
        ]
        result = subprocess.run(download_cmd, check=True, capture_output=True)
        print(result.stdout.decode())

        # Find downloaded file
        input_file = None
        for ext in ['mp4', 'webm', 'mkv']:
            if os.path.exists(f"input.{ext}"):
                input_file = f"input.{ext}"
                break
        if not input_file:
            return jsonify({"error": "Downloaded file not found"}), 500

        # Transcode to standard mp4
        output_file = "output.mp4"
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", "scale=720:-1",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-y",
            output_file
        ]
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)

        return jsonify({"status": "success", "output": output_file}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "stderr": e.stderr.decode() if e.stderr else ""
        }), 500

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
