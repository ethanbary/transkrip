from datetime import timedelta

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

import os

import whisper

def getaudiofile(videofile,audiofilename):
    video = VideoFileClip(videofile)
    audio = video.audio
    audio.write_audiofile(audiofilename)

def transcribe_audio(path):
    
    model = whisper.load_model("medium") # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(path)
    segments = transcribe['segments'] #Change this to your desired style segments/words
    
    print("making .srt file")
    
    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join("SrtFiles", f"{audiofile}sub.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

def addsubtovideo(videofile,audiofilename,finalvideoname):
   
    video = VideoFileClip(videofile)
    
    #adjust subtitle style
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=30, color='white')
    
    subtitle = SubtitlesClip(f"SrtFiles/{audiofilename}sub.srt",generator)
    
    video_with_sub = CompositeVideoClip([video,subtitle.set_pos(('center',1680))]) #adjust position
    
    video_with_sub.write_videofile(finalvideoname,codec='libx264', audio_codec="aac",)
    
    
#set file directory
videofile = "Screen Recording 2024-04-11 at 21.08.29.mov"
audiofile = "output/audio2.mp3"
finalvideoname="output/final2.mp4"

#from video to audio
print("[1/3] Seperating audio")
getaudiofile(videofile=videofile,audiofilename=audiofile)

#from audio to subtitle
print("[2/3] Transcribing")
transcribe_audio(audiofile)

#add subtitle back to video
print("[3/3] Adding subtitle to video")
addsubtovideo(videofile=videofile,audiofilename=audiofile,finalvideoname=finalvideoname)

