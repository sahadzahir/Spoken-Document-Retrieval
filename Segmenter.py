from pydub import AudioSegment
import vad
import os
import struct
import sys

class Segmenter():

    infile = None
    outpath = None
    temp = None
    name = None
    sp_start = []
    sp_end = [] 

    def __init__(self,inputfile, outputpath,name):
        self.infile=inputfile
        self.outpath = outputpath
        self.name =name

    def splitAudio(self,a, b,infile,outfile):
        "splits the audio file from t=a to t=b milliseconds"
        #path = "/Users/oem/Desktop/Segment"+str(++i)+".wav"
        #audio = AudioSegment.from_wav('C:\\Users\\oem\\Desktop\\test.wav')
        audio = AudioSegment.from_wav(infile)
        audio_segment = audio[a:b]
        audio_segment.export(outfile,format='wav')

    def segmentAudio(self,out):
        myvad = vad.VAD()
        fin = open((self.infile),'rb')
        fin.read(44)
        block = fin.read(4000)
        totsum = 0
        chunk_cnt = 0
        curr_chunk = []
        myvad.Init()
        i=0
        fo = open(out,'w')
        while len(block) != 0:
            samples = struct.unpack("=%ih" % (len(block)/2),block)

            events = myvad.DoVad(samples)
            time = None
            for framestamp,evt in events:
                time=int(framestamp*10)
                #print "%.3f " % (time*0.001)


                if evt == vad.VAD.SPSTART:
                    i+=1
                    #print self.name+"_kws_segment" +str(i)
                    fo.write(self.name+"_kws_segment" +str(i)+" ")
                    fo.write("%.3f " % (time*0.001))
                    temp = time
                    self.sp_start.append(time)
                else:
                    fo.write("%.3f\n" % (time*0.001))
                    self.splitAudio(temp,time,self.infile,self.outpath+os.sep+"Segment"+str(i)+".wav")
                    self.sp_end.append(time)


            block = fin.read(4000)

        self.splitAudio(temp,sys.maxint,self.infile,self.outpath+os.sep+"Segment"+str(i)+".wav")
        audio = AudioSegment.from_wav(self.infile)
        fo.write("%.3f " % (len(audio)*0.001))
        self.sp_end.append(len(audio))
        fo.close()


#segmenter = Segmenter("/Users/CardMaster/Desktop/hi.wav", "/Users/CardMaster/Desktop/Hi", name = "5mintest")
#segmenter.segmentAudio("/Users/CardMaster/Desktop/SEGMENTTIMESTEST.txt")