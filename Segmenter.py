from pydub import AudioSegment
import vad
import os
import struct
class Segmenter():

    infile = None
    outpath = None
    temp = None

    def __init__(self,inputfile, outputpath):
        self.infile=inputfile
        self.outpath = outputpath

    def splitAudio(self,a, b,infile,outfile):
        "splits the audio file from t=a to t=b milliseconds"
        #path = "/Users/oem/Desktop/Segment"+str(++i)+".wav"
        #audio = AudioSegment.from_wav('C:\\Users\\oem\\Desktop\\test.wav')
        audio = AudioSegment.from_wav(infile)
        audio_segment = audio[a:b]
        audio_segment.export(outfile,format='wav')

    def segmentAudio(self):
        myvad = vad.VAD()
        fin = open(os.path.abspath(self.infile),'rb')
        fin.read(44)
        block = fin.read(4000)
        totsum = 0
        chunk_cnt = 0
        curr_chunk = []
        myvad.Init()
        i=0
        while len(block) != 0:
            samples = struct.unpack("=%ih" % (len(block)/2),block)

            events = myvad.DoVad(samples)


            time = None
            for framestamp,evt in events:
                time=int(framestamp*10)
                print "%.3f " % (time*0.001),
                if evt == vad.VAD.SPSTART:
                    print " SPEECH START "
                    temp = time
                else:
                    print " SPEECH END "
                    i+=1
                    self.splitAudio(temp,time,self.infile,self.outpath+"\\Segment"+str(i)+".wav")

            block = fin.read(4000)

out = os.path.dirname(vad.__file__)
segmenter = Segmenter("C:\\Users\\oem\\Desktop\\test.wav",out)  # constructor for segmenter object
                                                                # takes in absolute paths for inputfile and output directory
segmenter.segmentAudio()  # does the segmentation
