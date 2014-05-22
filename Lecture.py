import  wx
import wx.media
from datetime import date




class Lecture():
	"Contains Information about Lectures Recorded"
	Topic=""
	Subject=""
	filePath=""
	Gender=""
	Date=date() #Default date


	def __init__(self):
		pass

	def getDate(self):
		return self.Date

	def getSubject(self):
		return self.Subject

	def getTopic(self):
		return self.Topic

	def getGender(self):
		return self.Gender

	def getFilePath(self):
		return self.filePath

	def setSubject(self, Subject):
		self.Subject=Subject

	def setDate(self,Date):
		self.Date=Date

	def setGender(self,Gender):
		self.Gender=Gender

	def setFilePath(self,filePath):
		self.filePath=filePath

	def setTopic(self,Topic):
		self.Topic=Topic


