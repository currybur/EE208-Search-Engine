import os
import speech_recognition as sr
from pydub import AudioSegment


def speech_recognition(path):
    r = sr.Recognizer()

    test = sr.AudioFile(path)

    with test as source:
        audio = r.record(source)

    result = r.recognize_google(audio, language='zh-CN')
    return result


def trans_mp3_to_wav(filename, filepath):
    song = AudioSegment.from_mp3(filepath)
    song.export(filename+".wav", format="wav")


def trans_flv_to_wav(filename,filepath):
    song = AudioSegment.from_flv(filepath)
    song.export(filename+".wav", format="wav")


def trans_raw_to_wav(filename,filepath):
    song = AudioSegment.from_raw(filepath)
    song.export(filename+".wav", format="wav")


def trans_m4a_to_wav(filename,filepath):
    cmd = "ffmpeg -i %s -ar 16000 %s"%(filepath,filename+'.wav')
    os.system(cmd)
