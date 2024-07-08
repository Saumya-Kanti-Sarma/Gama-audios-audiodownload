from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app) # using CORS to be able to fetch data easily

@app.route('/')
def hello_world():
    response = jsonify({
        "msg": "hello coders..",
        "Mp3": "https://audiodownload.onrender.com/api/mp3/link?url=",
        "Mp3_search": "https://audiodownload.onrender.com/api/mp3/info?search=",
        "mp4": "Processing..",
        "status": 200
    })
    response.headers.add("Content-Type", 'application/json')
    return response

@app.route('/api/mp3/link')
def get_audio_url():
    url = request.args.get('url')
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).get_by_itag(251)
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", "GamaAudios")

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        audio_file_path = audio_stream.download(output_path=download_path)
        base, ext = os.path.splitext(audio_file_path)
        new_file = base + '.mp3'
        os.rename(audio_file_path, new_file)

        audio_file_name = os.path.basename(new_file)

        return jsonify({
            "status-code": 200,
            "status": "download successful",
            "audio_url": f"https://audiodownload.onrender.com/download/{audio_file_name}"
        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code": 505,
            "status": "download unsuccessful"
        })

@app.route('/download/<filename>')
def download_file(filename):
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", "GamaAudios", filename)
    return send_file(download_path, as_attachment=True)

@app.route('/api/mp3/info')
def get_audio_info():
    search = request.args.get('search')
    try:
        yt = YouTube(search)
        thumbnail = yt.thumbnail_url
        views = yt.views
        title = yt.title
        channel = yt.channel_url
        description = yt.description
        keywords = yt.keywords
        publish_date = yt.publish_date
        return jsonify({
            "status-code": 200,
            "thumbnail": thumbnail,
            "views": views,
            "title": title,
            "channel": channel,
            "description": description,
            "keywords": keywords,
            "publish_date": publish_date,
        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code": 505,
            "status": "fetching info unsuccessful"
        })

if __name__ == '__main__':
    app.run(debug=True)
