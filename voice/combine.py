from voice.combined_tools import *

def recog(path):
    file = os.path.splitext(path)
    filename, type = file

    if type == ".mp3":
        filename = filename + "1"
        trans_mp3_to_wav(filename,path)
    elif type == ".flv":
        filename = filename + "1"
        trans_flv_to_wav(filename,path)  # mei you ce shi ji
    elif type == ".raw":
        filename = filename + "1"
        trans_raw_to_wav(filename,path)  # mei you ce shi ji
    elif type == ".m4a":
        filename = filename + "1"
        trans_m4a_to_wav(filename,path)

    result = speech_recognition(filename+".wav")
    return result

