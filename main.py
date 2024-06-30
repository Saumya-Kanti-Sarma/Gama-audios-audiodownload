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
        "Mp3": "/api/mp3/",
        "mp4": "Processing..",
        "status": 200
    })
    response.headers.add("Content-Type", 'application/json')
    return response

@app.route('/api/mp3/<id>')
def get_audio_url(id):
    # kJQP7kiw5Fk&pp=ygUJZGVzcGFjaXRv
    URL = f"https://www.youtube.com/watch?v={id}"
    try:
        yt = YouTube(f"{URL}")
        audio_streams = yt.streams.filter(only_audio=True).get_by_itag(251)
        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        folder = "GamaAudios"
        folder_path = os.path.join(download_path, folder)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        audio_file_path = audio_streams.download(output_path=folder_path)
        audio_file_name = os.path.basename(audio_file_path)

        return jsonify({
            "status-code" : 200,
            "status" : "download successfull",
            "audio_url": f"/download/{audio_file_name}"
        })

    except Exception as e:
        return jsonify({
            "We have an error": str(e),
            "status-code" : 505,
            "status" : "download un-successfull",
        })

@app.route('/download/<filename>')
def download_file(filename):
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", "GamaAudios", filename)
    return send_file(download_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
