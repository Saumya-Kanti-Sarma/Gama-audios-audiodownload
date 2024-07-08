from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app) #using CORS to be able to fetch data easily

@app.route('/')
def hello_world():
    response =  jsonify({
        "msg": "hello coders..",
        "Mp3": "https://audiodownload.onrender.com/api/mp3/link?url=",
        "mp4": "Processing..",
        "status": 200
    })
    response.headers.add("Content-Type", 'application/json')
    return response

@app.route('/api/mp3/link')
def get_audio_url():
    # kJQP7kiw5Fk&pp=ygUJZGVzcGFjaXRv
    url = request.args.get('url')
    URL = url
    try:
        yt = YouTube(URL)
        audio_streams = yt.streams.filter(only_audio=True).get_by_itag(251)
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        audio_file_path = audio_streams.download(output_path=download_path)
        base, ext = os.path.splitext(audio_file_path) 
        new_file = base + '.mp3'
        os.rename(audio_file_path, new_file) 

        return jsonify({
            "status-code" : 200,
            "status" : "download successfull",
        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code" : 505,
            "status" : yt.title + " download un-successfull",
        })

@app.route('/api/mp3/info')
def get_audio_info():
    search = request.args.get('search')
    URL = search
    try:
        yt = YouTube(URL)
        thumbnail = yt.thumbnail_url
        views = yt.views
        title = yt.title
        channel = yt.channel_url
        description = yt.description
        keyword = [yt.keywords]
        publish_date = yt.publish_date
        return jsonify({
            "status-code" : 200,
            "thumbnail" : thumbnail,
            "views" : views,
            "title" : title,
            "channel" : channel,
            "description" : description,
            "keyword" : keyword,
            "publish_date" : publish_date,

        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code" : 505,
            "status" : yt.title + " download un-successfull",
        })

if __name__ == '__main__':
    app.run(debug=True)
