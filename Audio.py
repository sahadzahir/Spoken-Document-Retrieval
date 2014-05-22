
class Audio():
	""
	# only handles 16khz, 16-bit depth Little Endian

	def __init__(self):
		self.sampleRate=0
		self.Duration_milli=0
		self.utteranceList=[]
		self.filePath=""

	def getRate(self):
		return self.sampleRate

	def getDuration(self):
		return self.Duration_milli

	def getData(self):
		fin=open(self.filePath)
		B=fin.read()
		samples = struct.unpack(">h",B)
		return samples
		pass #Forgot what this method is for
	
		



