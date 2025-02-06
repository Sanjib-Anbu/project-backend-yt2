from flask import Flask, request, Response
import yt_dlp
import io

app = Flask(__name__)

@app.route('/download')
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')

    if not url or format_type not in ['mp3', 'mp4']:
        return {"error": "Invalid request"}, 400

    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format_type == 'mp3' else [],
        'outtmpl': '-',  # "-" tells yt-dlp to write to stdout (in memory)
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        buffer = io.BytesIO()
        ydl.download([url])
        buffer.seek(0)

    mime_type = 'audio/mpeg' if format_type == 'mp3' else 'video/mp4'
    
    return Response(buffer, mimetype=mime_type, headers={
        'Content-Disposition': f'attachment; filename="download.{format_type}"'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
