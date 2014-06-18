from pydub import AudioSegment

def splitAudio(a, b):
    "splits the audio file from t=a to t=b milliseconds"
    path = "/Users/oem/Desktop/hi.wav"
    audio = AudioSegment.from_wav('C:\\Users\\oem\\Documents\\Recordings\\Evo Bio\\000311_0015.wav')
    audio_segment = audio[a:b]
    audio_segment.export(path,format='wav')



splitAudio(1700000, 1730000)





