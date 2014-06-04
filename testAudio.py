from pydub import AudioSegment

	
def splitAudio(a, b):
	"splits the audio file from t=a to t=b milliseconds"
	path = "/Users/CardMaster/Desktop/hi.wav"
	audio = AudioSegment.from_wav("/Users/CardMaster/Dropbox/SMP 2014/background/time-frequency-lab/stimuli_lab/example5.wav")
	audio_segment = [100]
	audio_segment[0] = audio[:b]
	audio_segment[0].export(path, format="wav")
	audio = AudioSegment.from_wav(path)
	a = (len(audio)-a)
	audio_segment[0] = audio[a:]
	audio_segment[0].export(path, format="wav")

splitAudio(1000, 2000)





