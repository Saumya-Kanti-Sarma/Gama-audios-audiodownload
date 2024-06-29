from pytube import YouTube


yt = YouTube("https://youtu.be/JDglMK9sgIQ?si=E_-U5vROnsrKhjvr")
audio_name = yt.title

print(audio_name)