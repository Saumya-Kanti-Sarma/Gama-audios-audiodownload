from flask import Flask, jsonify, send_file
from flask_cors import CORS
from pytubefix import YouTube

app = Flask(__name__)
CORS(app) # using CORS to be able to fetch data easily

@app.route('/')
def hello_world():
    response = jsonify({
        "msg": "hello coders..",
        "status": 200,
    })
    response.headers.add("Content-Type", 'application/json')
    return response

@app.route('/api/mp3/<path:url>')
def get_audio_url(url):
    try:
        validUrl = "https://youtu.be/" + url
        yt = YouTube(validUrl,use_po_token=True)
        audio_stream = [
            {
                "itag": streams.itag,
                "mime_type": streams.mime_type,
                "url": "https://youtu.be/" + url,
            }
            for streams in yt.streams.filter(only_audio=True,mime_type="audio/mp4")
        ]
        return jsonify({
            "status-code": 200,
            "streams":audio_stream
        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code": 505,
        })

@app.route("/download/itag/<path:itag>/<path:url>")
def download(itag, url):
    try:
        validUrl = "https://youtu.be/" + url
        yt = YouTube(validUrl, use_po_token=True)
        download_stream = yt.streams.get_by_itag(itag)
        
        # Get the direct download URL
        download_url = download_stream.url
        
        return jsonify({
            "status": 200,
            "downloadUrl": download_url
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 505
        })
if __name__ == '__main__':
    app.run()
