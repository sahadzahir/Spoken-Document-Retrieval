
class Decoder():
	"Stub for generating lattices from audio"

	def __init__(self):
		pass

	def DecodeLecture(self,Lecture):
		"grabs audio from the lecture to decode"
		audio=Lecture.GetAudio()
		if audio!=None:
			return self.DecodeAudio(audio)

	def DecodeAudio(self,Audio):
		"send the audio to server and get back a lattice."
		# input: Audio - an audio object 
		pass

	def AudioLength(self):
		pass
