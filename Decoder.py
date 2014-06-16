
import gzip
from ftplib import FTP
import os
import distutils.core
import tarfile

class Decoder():
	"Stub for generating lattices from audio"

	def __init__(self):
		pass

	def DecodeAudio(self, filePath):
		"send the audio to server and get back a lattice."
		# input: filePath of segmented Audio
		# original audio is copied to directory inside project file
		#segmented audio will be located in audio/ under project directory
		tar = tarfile.open( "compressedAudio/"+"compressedAudio.tar.gz", "w:gz" )
		tar.add("audio/")
		tar.close()
		fileList = os.listdir(os.path.abspath("audio/"))
		for fileName in fileList:
			os.remove(os.path.abspath("audio/")+"/"+fileName)

		#Deletes all the segmented audio from audio/ after gzip


	def AudioLength(self):
		pass


d = Decoder()
d.DecodeAudio("/Users/CardMaster/Dropbox/SMP 2014/background/time-frequency-lab/stimuli_lab")
