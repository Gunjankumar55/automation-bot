from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    data = request.get_json()
    if not data or 'videoId' not in data:
        return jsonify({"error": "Missing 'videoId'"}), 400

    video_id = data['videoId']
    title = data.get('title', 'Untitled')
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Download video using yt-dlp with cookies
        download_cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "mp4",
            "-o", "input.%(ext)s",
            youtube_url
        ]
        result = subprocess.run(download_cmd, check=True, capture_output=True)
        print(result.stdout.decode())

        # Check for downloaded file
        input_file = "input.mp4"
        if not os.path.exists(input_file):
            input_file = "input.webm"
        if not os.path.exists(input_file):
            return jsonify({"error": "Downloaded file not found"}), 500

        # Process with ffmpeg: resize to 720 width
        output_file = "output.mp4"
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", "scale=720:-1",
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
