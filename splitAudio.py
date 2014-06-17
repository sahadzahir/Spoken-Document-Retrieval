from pydub import AudioSegment

def splitAudio(a, b):
    "splits the audio file from t=a to t=b milliseconds"
    path = "/Users/oem/Desktop/hi.wav"
    audio = AudioSegment.from_wav('C:\\Users\\oem\\Documents\\Recordings\\Evo Bio\\000311_0015.wav')
    # audio_segment = [100]
    # audio_segment[0] = audio[:b]
    # audio_segment[0].export(path, format="wav")
    # audio = AudioSegment.from_wav(path)
    # a = (len(audio) - a)
    # audio_segment[0] = audio[a:]
    # audio_segment[0].export(path, format="wav")

    audio_segment = audio[a:b]
    audio_segment.export(path,format='wav')



splitAudio(600000, 610000)





