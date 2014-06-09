import wx
import numbers

class Lattice():
	#-- TOFIX : What data structure should you use for this - BP

	def __init__(self):
		self.edgeList = []

	def parseFile(self, name):
		"Parses lattice file and stores data"
		i = 0
		j = 0
		nodelbl1 = []
		nodelbl2 = []
		worldlbl = []
		latticeID = []
		langModelScore = []
		acousticModelScore = []
		frameAlignment = []
		path = "doc/" + name
		fo = open(path, "r")
		for line in fo:
			if i == 0:
				latticeID.append(line)
			elif line == '\n':
				i = -1
			else:

				# This ignores the values at the end of the lattice
				if line.split(" ")[0].isdigit():
					nodelbl1.append(int(line.split(" ")[0]))

				if line.split(" ")[1].isdigit():
					nodelbl2.append(int(line.split(" ")[1]))		

				if not line.split(" ")[2] == '\n':
					worldlbl.append(line.split(" ")[2])
					langModelScore.append(float(line.split(" ")[3].split(",")[0]))
					acousticModelScore.append(float(line.split(" ")[3].split(",")[1]))
					# This removes blank spaces and casts all the elements of the list to int before appending 
					frameAlignment.append([map(int, [x for x in line.split(" ")[3].split(",")[2].split("_") if x])])
					# frameAlignment is a 2d list
			i+=1	
		fo.close();





	

