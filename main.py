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
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Download best video+audio using yt-dlp with cookies
        download_cmd = [
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-f", "bv*+ba/b",
            "-o", "input.%(ext)s",
            youtube_url
        ]
        result = subprocess.run(download_cmd, check=True, capture_output=True)
        print(result.stdout.decode())

        # Check if file exists
        input_file = None
        for ext in ['mp4', 'mkv', 'webm']:
            possible_file = f"input.{ext}"
            if os.path.exists(possible_file):
                input_file = possible_file
                break

        if not input_file:
            return jsonify({"error": "Downloaded file not found"}), 500

        # Process with FFmpeg to 9:16 format for Shorts
        output_file = "output.mp4"
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_file,
            "-vf", "scale=720:1280,setsar=1",
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
        return jsonify({"status": "error", "message": str(e)}), 500
