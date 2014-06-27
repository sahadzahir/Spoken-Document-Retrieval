import wx

class Edge():

    nodelbl1 = None
    nodelbl2 = None
    wordlbl = None
    latticeID = None
    langModelScore = None
    acousticModelScore = None
    frameAlignment = []
    startTime = None
    endTime = None
    length = None

    def __init__(self,node1,node2,word,ID,lmscore,amscore,alignment):
        self.nodelbl1 = node1
        self.nodelbl2 = node2
        self.wordlbl = word
        self.latticeID = ID
        self.langModelScore = lmscore
        self.acousticModelScore = amscore
        self.frameAlignment = alignment

    def toString(self):
        return ""+str(self.nodelbl1) + str(self.nodelbl2) + str(self.wordlbl) + str(self.latticeID) + str(self.langModelScore) + str(self.acousticModelScore) + str(self.frameAlignment)

    def setStartTime(self, startTime):
        self.startTime = startTime

    def setEndTime(self, endTime):
        self.endTime = endTime

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime
    def getWordlbl(self):
        return self.wordlbl
    def getLatticeID(self):
        return self.latticeID

