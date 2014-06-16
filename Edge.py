import wx

class Edge():

    nodelbl1 = None
    nodelbl2 = None
    wordlbl = None
    latticeID = None
    langModelScore = None
    acousticModelScore = None
    frameAlignment = None

    def __init__(self,node1,node2,word,ID,lmscore,amscore,alignment):
        self.nodelbl1 = node1
        self.nodelbl2 = node2
        self.wordlbl = word
        self.latticeID = ID
        self.langModelScore = lmscore
        self.acousticModelScore = amscore
        self.frameAlignment = alignment

