import wx
import numbers
import Edge

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
        frameAlignment = None

        path = "doc/" + name
        fo = open(path, "r")
        for line in fo:
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
                    frameAlignment = [map(int, [x for x in line.split(" ")[3].split(",")[2].split("_") if x])]
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


# lattice = Lattice()
# lattice.parseFile("lattice.txt")
# print lattice.getEdgeList()[33].toString()
# print lattice.getInvertedIndex()






