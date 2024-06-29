from pytube import YouTube
from flask import Flask, request, jsonify


app = Flask(__name__)
@app.route("/",  methods=['GET'])
def Home():
    return jsonify({
        "msg" : "welcome to my free youtube download api",
        "founder" : "Saumya Kanti Sarma",
        "company" : "Gama Technologies Private Limited",
        "audioDownload":{
            "api": "https://gamaaudios/api/audiodownload/:(HERE PASTE THE VIDEO ID)",
            "example-video-link": "https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "videoID": "JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
        },
        "videoDownload":{
            "msg": "Server under maintainance..",
            "api": "https://gamaaudios/api/videodownload/:(HERE PASTE THE VIDEO ID)",
            "example-video-link": "https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "videoID": "JDglMK9sgIQ?si=E_-U5vROnsrKhjvr",
            "quality":{
                "360p": "https://gamaaudios/api/videodownload/:id/360p",
                "480p": "https://gamaaudios/api/videodownload/:id/480p",
                "720p": "https://gamaaudios/api/videodownload/:id/720p",
                "1080p": "https://gamaaudios/api/videodownload/:id/1080p",
            }
        },
        "aboutFounder":{
            "name":"saumya kanti sarma",
            "gmail" : "saumyakatisarma2004@gmail.com",
            "github" : "https://github.com/Saumya-Kanti-Sarma",
            "instagram" : "https://www.instagram.com/serean_miles/",
            "msg":"in case need, feel free to contact me!..."
        }
    })


@app.route("/api/audiodownload/<video_id>", methods=['GET'])
def download_audio(video_id):
    try:
        yt = YouTube(f"https://youtu.be/{video_id}")
        audio_stream = yt.streams.filter(only_audio=True).get_by_itag(140)
        
        if audio_stream:
            audio_stream.download()
            return jsonify({"message": "Audio download successfully"}), 200
        else:
            return jsonify({"error": "Audio stream not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


  # https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr
  # https://youtu.be/ZQkb7fCr2bQ?si=p8EIQzzi-wv5phhU