from flask import Flask, request, jsonify, send_file
import os
import pytube
import ffmpeg

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    format_type = request.args.get("format", "mp4")

    if not url:
        return jsonify({"error": "Missing YouTube video URL"}), 400

    try:
        yt = pytube.YouTube(url)
        if format_type == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            filename = f"{yt.title}.mp3"
            audio_stream.download(filename=filename)

            # Convert to mp3 using ffmpeg
            mp3_file = filename.replace(".mp4", ".mp3")
            ffmpeg.input(filename).output(mp3_file, format='mp3').run(overwrite_output=True)
            os.remove(filename)  # Remove original file

            return send_file(mp3_file, as_attachment=True)

        else:
            video_stream = yt.streams.get_highest_resolution()
            filename = f"{yt.title}.mp4"
            video_stream.download(filename=filename)
            return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
   
