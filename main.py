from flask import Flask, jsonify
from pytube import YouTube
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def hello_world():
    return jsonify({
        "msg" : "hello coders.."
    })

@app.route('/api/<id>')
def downloadMusic(id):
  URL = f"https://youtu.be/{id}"
  try:
    yt = YouTube(f"{URL}")
    audio_streams = yt.streams.filter(only_audio=True).get_by_itag(251)
    audio_name = f"{yt.title}_From_Gama_Audios_"

    # declearing download path
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    folder = "GamaAudios"
    folder_path = os.path.join(download_path,folder)

    # declearing logging infos
    logging.info(f"Download path: {download_path}")
    logging.info(f"Folder path: {folder_path}")
    
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      logging.info(f"Created folder: {folder_path}")

      
    audio_streams.download(output_path=folder_path)

    return jsonify({
       "Title" : audio_name,
       "quality" : str(audio_streams),
       "status" : 200
    })

  except Exception as e:
    return jsonify({
        "We have a error" : e
    })


if __name__ == '__main__':
    app.run(debug=True)
