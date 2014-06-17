#!/usr/bin/python
""" Simple VAD module - author BP
   
usage: vad.py [file.wav]
"""

import sys,os,struct,math

UseEndpointing = False
DEBUG=False
vad_out_template="chunked/chunk%05i.pcm"

class VAD:
    "Implements a simple energy based VAD"
    
    STATE_SIL     = 0
    STATE_SPEECH  = 1
    STATE_PAUSE   = 2
    
    SPSTART  = 1        # indicates start of speech
    SPEND    = 2        # indicates end of speech

    def __init__(self):
        self.threshold=0
        self.frame_size = 400;    # please tune these defaults accordingly
        self.frame_step = 160;
        self.threshold = 300;
        self.hangover_threshold = 50;   # 50 frame for short segments
        self.buffer = []
        self.frame_cnt = -1;
        self.Init()

    def Init(self):
        "Initializes the VAD"
        self.state =  VAD.STATE_SIL
        self.frame_cnt = -1;
        self.cdata = [] 

    def ProcessFrame(self,frame):
        "Processes a speech frame, returns True if it is a speech frame"
        " false if not."
        # a speech frame is a list of shorts
        self.frame_cnt = self.frame_cnt+1
        energy = math.sqrt(sum(map(lambda(x): x*x, frame))/float(len(frame)))
        self.frame_energy = energy
        #print "%i %f" % (self.frame_cnt,self.frame_energy)
        if energy>self.threshold: return True

    def CheckState(self,isSpeechFrame):
        "update the state machine for the VAD, returning events if detected"
        events = []
        if self.state == VAD.STATE_SIL:
            if isSpeechFrame:
                self.state = VAD.STATE_SPEECH
                events.append((self.frame_cnt,VAD.SPSTART))
            else:
                pass
        elif self.state == VAD.STATE_SPEECH:
            if not isSpeechFrame:
                self.state = VAD.STATE_PAUSE
                self.hangover = 0
            else:
                pass
        elif self.state == VAD.STATE_PAUSE: 
            # hangover state - if we see a speech frame, recover
            if isSpeechFrame:
                self.state = VAD.STATE_SPEECH
            else:
                self.hangover = self.hangover + 1
                if self.hangover > self.hangover_threshold:
                    events.append((self.frame_cnt,VAD.SPEND))
                    self.state = VAD.STATE_SIL
        return events

    def DoVad(self,buffer):
        "Performs VAD, returning a list of changepoints and events"
        # initialize a list of events in this buffer
        events = []

        # add samples to a temp buffer
        self.buffer.extend(buffer)
        while len(self.buffer)> self.frame_size:
            # window and test a frame
            window = self.buffer[:self.frame_size]
            self.buffer = self.buffer[self.frame_step:]
            isSpeech = self.ProcessFrame(window)
            events.extend( self.CheckState(isSpeech) )

        return events

    def Chop(self,buffer):
        "Returns a sequence of chopped, marked buffers - "
        " each buffer is a tuple, containing data chunk and end of speech mark"
        " a data chunk itself is a list of integer samples"
        " if it is the end of the speech chunk, the eos mark is true"

        self.buffer.extend(buffer)
        chunks = []

        while len(self.buffer)>self.frame_size:
            data = self.buffer[:self.frame_step] # get data frame

            window = self.buffer[:self.frame_size] # get frame for thresholding
            self.buffer = self.buffer[self.frame_step:] # advance buffer

            isSpeech = self.ProcessFrame(window)
            events = self.CheckState(isSpeech) 
        
            if self.state == VAD.STATE_SPEECH or self.state == VAD.STATE_PAUSE:
                # speech, add to the current kkkkkkkkkkkkkkhunk
                if len(events)>0: 
                    if DEBUG: print "mark start", events, len(self.cdata), len(data) , self.frame_cnt
                self.cdata.extend(data)
            else: # silence 
                if len(events)>0:
                    if DEBUG: print "mark end: " , events, self.frame_cnt
                    # end of speech marker detected
                    chunks.append( (True,self.cdata) )
                    self.cdata = [] 

        # haven't seen endpoint yet
        # pack as much of the chunk as possible
        if len(self.cdata)>0:
            chunks.append( (False,self.cdata) )
            self.cdata = []

        return chunks


if __name__ == '__main__':
    # test the vad against a file
    myvad = VAD()

    if len(sys.argv)<2:
        print __doc__
        sys.exit(1)

    # open file, read block by block 
    in_snd_file = sys.argv[1]
    fin = open(in_snd_file,'rb')
    fin.read(44) 
    block = fin.read(4000)

    totsum = 0
    chunk_cnt = 0
    curr_chunk = [] 
    myvad.Init()
    while len(block) != 0:
        samples = struct.unpack("=%ih" % (len(block)/2),block)

        if not UseEndpointing:
            chunks = myvad.Chop(samples)
            for isEnd,chunk in chunks:
                curr_chunk.extend(chunk)
                totsum = totsum +len(chunk)
                if isEnd: 
                    chunk_cnt = chunk_cnt+1
                    fout=open(vad_out_template % chunk_cnt,'wb')
                    for sample in curr_chunk: 
                        fout.write(struct.pack('=h',sample))
                    fout.close()

                    print "samples: %i len: %.3f" % (totsum, totsum/16000.0)
                    curr_chunk = []
                    totsum = 0
        else: 
            events = myvad.DoVad(samples)
            for framestamp,evt in events:
                time=framestamp*0.01 # Time in seconds
                print "%.3f " % time,
                if evt == VAD.SPSTART:
                    print " SPEECH START "
                else:
                    print " SPEECH END "

        block = fin.read(4000)
        
        
