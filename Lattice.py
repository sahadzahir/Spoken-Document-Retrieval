import wx
import numbers
import Edge
import Segmenter

class Lattice():

    edgeList = []
    invertedIndex = {}


    def __init__(self):
        pass
    def getEdgeList(self):
        return self.edgeList
    def getInvertedIndex(self):
        return self.invertedIndex
    def parseFile(self, name):
        "Parses lattice file and stores data"
        i = 0
        j = 0


        # temp variables to create edge
        nodelbl1 = None
        nodelbl2 = None
        wordlbl = None
        latticeID = None
        langModelScore = None
        acousticModelScore = None
        frameAlignment = []
        isRepeat = 0
        path = name
        fo = open(path, "r")
        for line in fo:
            if line in ['\n','\r','\r\n','\n\r']:
                isRepeat = 1-isRepeat
            if isRepeat == 0:
                if i == 0:
                    latticeID = line
                elif line == '\n':
                    i = -1
                else:

                    # This ignores the values at the end of the lattice
                    if line.split(" ")[0].isdigit():
                        nodelbl1 = int(line.split(" ")[0])

                    if line.split(" ")[1].isdigit():
                        nodelbl2 = int(line.split(" ")[1])

                    if not line.split(" ")[2] == '\n':
                        wordlbl = line.split(" ")[2]
                        langModelScore = float(line.split(" ")[3].split(",")[0])
                        acousticModelScore = float(line.split(" ")[3].split(",")[1])
                        # This removes blank spaces and casts all the elements of the list to int before appending
                        frameAlignment = map(int, [x for x in line.split(" ")[3].split(",")[2].split("_") if x])
                        # frameAlignment is a 2d list
                i += 1
                edge = Edge.Edge(nodelbl1,nodelbl2,wordlbl,latticeID,langModelScore,acousticModelScore,frameAlignment)
                #print edge.toString()
                self.edgeList.append(edge)
                if not self.invertedIndex.has_key(wordlbl):
                    self.invertedIndex[wordlbl] = []
                self.invertedIndex[wordlbl].append(j)
                j += 1
        fo.close()


lattice = Lattice()
lattice.parseFile("result2.txt")
length = 0
lengthList = []

lattice.getEdgeList()[0].frameAlignment = []

s = Segmenter.Segmenter("/Users/CardMaster/Desktop/hi.wav", "/Users/CardMaster/Desktop/Hi", name = "5mintest")
s.segmentAudio("/Users/CardMaster/Desktop/SEGMENTTIMESTEST.txt")
lattice.getEdgeList().pop(0)
for edge in lattice.getEdgeList():
    for frame in edge.frameAlignment:
        length+=1
    length *= 10
    lengthList.append(length)    
    length = 0
print lengthList
# Initialize list
time_at_node = [0 for i in range(1000000)]

i = 0
j = 0
tempEdge = Edge.Edge(None, None, None, None, None, None, None) 

for edge in lattice.getEdgeList():
    print str(edge.nodelbl1)+"-" +str(edge.nodelbl2)

    #if i == 0:
        #edge.setStartTime(s.sp_start[int(edge.getLatticeID().split("Segment")[1])-1])
        #edge.setEndTime(lengthList[i]+edge.getStartTime())
    if not (tempEdge.getLatticeID() == edge.getLatticeID()):
        edge.setStartTime(s.sp_start[int(edge.getLatticeID().split("Segment")[1])-1])
        edge.setEndTime(lengthList[i]+edge.getStartTime())
        #print str(tempEdge.nodelbl1)+"-"+str(tempEdge.nodelbl2)+":"+str(edge.nodelbl1)+"-"+str(edge.nodelbl2)
        #print tempEdge.toString() + "-"+edge.toString()
    else:
        if not (edge.nodelbl1 == tempEdge.nodelbl1):
            edge.setStartTime(tempEdge.getEndTime())
            edge.setEndTime(lengthList[i]+edge.getStartTime())
        else:
            # If another edge branches from same starting node 
            edge.setStartTime(tempEdge.getStartTime())
            edge.setEndTime(lengthList[i]+edge.getStartTime())

            #print j
    tempEdge = edge
    i+=1
    j+=1


i = 0
for edge in lattice.getEdgeList():
#     time_at_node[edge.nodelbl2] = time_at_node[edge.nodelbl1] + (lengthList[i])
    print str(edge.getStartTime()) + " - " + str(edge.getEndTime()) +"-"+str(i)+"-"+str(edge.getWordlbl())
    i+=1

print i
#print time_at_node[1] 
#print lattice.getEdgeList()[0].getStartTime()






