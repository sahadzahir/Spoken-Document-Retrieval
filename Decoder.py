
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

		tar = tarfile.open( filePath+"compressedAudio.tar.gz", "w:gz" )
		tar.add("audio/")
		tar.close()

		# Connects to ftp server

		ftp = FTP()
		ftp.connect(host='192.122.139.244', port=7010)
		ftp.login('sahad', 'R33pydLj')
 
		upload_file_path = filePath+"compressedAudio.tar.gz"

		# Sending the gzip file through ftp

		#Open the file
		try:
			upload_file = open(upload_file_path, 'r')

			#get the name
			path_split = upload_file_path.split('/')
			final_file_name = path_split[len(path_split)-1]

			#transfer the file
			print('Uploading ' + final_file_name + '...')

			ftp.storbinary('STOR '+ final_file_name, upload_file)

			print('Upload finished.')

		except IOError:
			print ("No such file or directory... passing to next file")

		# Retrieving the file from ftp server

		# Open the file for writing in binary mode
		#print 'Opening local file ' + filename
		#file = open(filename, 'wb')

		# Download the file a chunk at a time
		# Each chunk is sent to handleDownload
		# We append the chunk to the file and then print a '.' for progress
		# RETR is an FTP command

		#print 'Getting ' + filename
		#ftp.retrbinary('RETR %s' % filename, file.write)

		# Clean up time
		#print 'Closing file ' + filename
		#file.close()




		#Deletes all the segmented audio from audio/ after gzip
		#fileList = os.listdir(os.path.abspath("audio/"))
		#for fileName in fileList:
		#	os.remove(os.path.abspath("audio/")+"/"+fileName)

	def AudioLength(self):
		pass


d = Decoder()
d.DecodeAudio("compressedAudio/")
