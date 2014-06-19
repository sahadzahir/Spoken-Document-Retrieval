from pydub import AudioSegment
import vad
import os
import struct

infile = "/Users/CardMaster/Desktop/hi.wav"
i=0
temp = None

def __init__(input):
    infile=input

def splitAudio(a, b,infile,outfile):
    "splits the audio file from t=a to t=b milliseconds"
    #path = "/Users/oem/Desktop/Segment"+str(++i)+".wav"
    #audio = AudioSegment.from_wav('C:\\Users\\oem\\Desktop\\test.wav')
    audio = AudioSegment.from_wav(infile)
    audio_segment = audio[a:b]
    audio_segment.export(outfile,format='wav')



# test the vad against a file
myvad = vad.VAD()

fin = open(os.path.abspath("/Users/CardMaster/Desktop/hi.wav"),'rb')
fin.read(44)
block = fin.read(4000)

totsum = 0
chunk_cnt = 0
curr_chunk = []
myvad.Init()
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
            splitAudio(int(temp),time,infile,"/Users/CardMaster/Desktop/Segment"+str(i)+".wav")


    block = fin.read(4000)

