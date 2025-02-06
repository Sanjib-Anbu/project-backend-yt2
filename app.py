from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    format_type = request.args.get('format', 'mp4')  # Default to MP4 if not specified

    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    ydl_opts = {
    'cookiefile': 'cookies.txt',  
    'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }] if format_type == 'mp3' else [],
    'ffmpeg_location': '/usr/bin/ffmpeg',  # Specify FFmpeg path
    'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),  
    'noplaylist': True,
}


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        return jsonify({'message': 'Download successful', 'file': file_name})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
