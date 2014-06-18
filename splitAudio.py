from pydub import AudioSegment

i = 0
def splitAudio(a, b,infile,outfile):
    "splits the audio file from t=a to t=b milliseconds"
    #path = "/Users/oem/Desktop/Segment"+str(++i)+".wav"
    #audio = AudioSegment.from_wav('C:\\Users\\oem\\Desktop\\test.wav')
    audio = AudioSegment.from_wav(infile)
    audio_segment = audio[a:b]
    audio_segment.export(outfile,format='wav')



splitAudio(0, 10000,'C:\\Users\\oem\\Desktop\\test.wav',"/Users/oem/Desktop/Segment"+str(++i)+".wav")





