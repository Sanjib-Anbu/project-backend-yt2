from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    format = request.args.get("format", "mp4")

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        ydl_opts = {
            "format": "bestaudio/best" if format == "mp3" else "bestvideo+bestaudio",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}] if format == "mp3" else [],
            "outtmpl": "downloads/%(title)s.%(ext)s"
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({"message": "Download complete", "file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
