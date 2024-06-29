from pytube import YouTube
from flask import Flask, request, jsonify, send_from_directory
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=['GET'])
def Home():
    return jsonify({
        "msg": "Welcome to my free YouTube download API",
        "founder": "Saumya Kanti Sarma",
        "company": "Gama Technologies Private Limited",
        "audioDownload": {
            "api": "https://gamaaudios/api/audiodownload/:(HERE PASTE THE VIDEO ID)",
            "example-video-link": "https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "videoID": "JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
        },
        "videoDownload": {
            "msg": "Server under maintenance..",
            "api": "https://gamaaudios/api/videodownload/:(HERE PASTE THE VIDEO ID)",
            "example-video-link": "https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "videoID": "JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "quality": {
                "360p": "https://gamaaudios/api/videodownload/:id/360p",
                "480p": "https://gamaaudios/api/videodownload/:id/480p",
                "720p": "https://gamaaudios/api/videodownload/:id/720p",
                "1080p": "https://gamaaudios/api/videodownload/:id/1080p",
            }
        },
        "aboutFounder": {
            "name": "Saumya Kanti Sarma",
            "gmail": "saumyakatisarma2004@gmail.com",
            "github": "https://github.com/Saumya-Kanti-Sarma",
            "instagram": "https://www.instagram.com/serean_miles/",
            "msg": "In case you need, feel free to contact me!..."
        }
    })

@app.route("/api/<video_id>", methods=['GET'])
def download_audio(video_id):
    try:
        yt = YouTube(f"https://youtu.be/{video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_name = yt._title
        
        if audio_stream:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            # Download the audio to the temporary directory
            audio_stream.download(output_path=temp_dir, filename=f"{video_id}.mp3")
            return send_from_directory(temp_dir, f"{audio_name}.mp3", as_attachment=True)
        else:
            return jsonify({"error": "Audio stream not found","status":404})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
