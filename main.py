from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    video_id = data.get("videoId")
    title = data.get("title", "untitled")

    if not video_id:
        return jsonify({"error": "Missing videoId"}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    input_file = "input.mp4"
    output_file = "output.mp4"

    try:
        subprocess.run(["yt-dlp", "-f", "best", "-o", input_file, video_url], check=True)
        subprocess.run(["ffmpeg", "-i", input_file, "-vf", "scale=720:-1", output_file], check=True)
        return jsonify({"status": "success", "output": output_file})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
