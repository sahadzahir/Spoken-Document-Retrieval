#!/usr/bin/python
"""
Authors: Sahad, Shashvat
Last updated:    Thu, May 22, 2014  5:06:55 PM
"""

import  wx
import  images
import wx.media
import wave

FRAMETB = True
TBFLAGS = ( wx.TB_HORIZONTAL			# toolbar arranges icons horizontally
            | wx.NO_BORDER			# don't show borders
            | wx.TB_FLAT			# 
            #| wx.TB_TEXT			# 
            #| wx.TB_HORZ_LAYOUT			
            )

#---------------------------------------------------------------------------


class TestToolBar(wx.Frame):
    "Creates UI for Program"
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Test ToolBar', size=(600, 400))

        self.panel  = wx.Panel(self)
        self.player = wx.media.MediaCtrl(self.panel)
        self.sizer  = wx.GridBagSizer(hgap=10, vgap=5)

        # Receive Search Inputs
        tc0 = wx.TextCtrl(self.panel, size=(175, 25))
        self.sizer.Add(tc0, pos=(0, 2), border=15, span=(1, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM)

        # Separator Line
        line = wx.StaticLine(self.panel)
        self.sizer.Add(line, pos=(3, 0), span=(1, 5),flag=wx.EXPAND|wx.BOTTOM, border=10)

        # Play Button Image converted to Bitmap
        imageFile = "button_play.png"
        self.image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        # Pause Button Image converted to Bitmap
        imageFile2 = "button_pause.png"
        self.image2 = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        # Scroller 
        #scroll = wx.ScrolledWindow(self, -1)
        #scroll.SetScrollbars(1, 1, 1200, 800)

        # Array of 'Play' Bitmap Buttons
        Play_Array = []

        #Array of sliders
        Slider_Array = []
        #ScrollBar(parent, pos=(100,100), size=(100,100),
        #style=SB_HORIZONTAL,name="ScrollBar")

        #for loop that creates sliders and play buttons
        for i in range (10):
            self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image1, size = (self.image1.GetWidth()+4, self.image1.GetHeight()+4), style=wx.NO_BORDER)
            self.play.Bind(wx.EVT_BUTTON, self.playFile)
            Play_Array.append(self.play)  
            self.sizer.Add(self.play, pos=((i+4), 0), flag=wx.ALIGN_CENTER_VERTICAL) 
            slider = wx.Slider(self.panel, wx.ID_ANY, size = (300,-1))
            slider.Bind(wx.EVT_SLIDER,self.Seek) 
            Slider_Array.append(slider)
            self.sizer.Add(slider, pos=((i+4), 2))    
        self.sizer.AddGrowableCol(2)
        self.panel.SetSizer(self.sizer)

        if FRAMETB:
            tb = self.CreateToolBar( TBFLAGS )
        else:
            tb = wx.ToolBar(client, style=TBFLAGS)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(tb, 0, wx.EXPAND)
            client.SetSizer(sizer)
            
        self.CreateStatusBar()

        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)

        tb.SetToolBitmapSize(tsize)

        #tb.AddSimpleTool(10, open_bmp, "Open", "Long help for 'Open'")
        tb.AddLabelTool(10, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.openFile, id=10)

        tb.AddSeparator()
        cbID = wx.NewId()

        tb.AddStretchableSpace()

        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        tb.Realize()
        self.Show()

    def openFile(self, event):
        "Opens File Dialog for choosing media file"
        msg = wx.FileDialog(self, message = "Open a media file",
                               style = wx.OPEN,
                               wildcard = "Media Files|*.wma;*.mp3;*.avi;*.wav")
        if msg.ShowModal() == wx.ID_OK:
            path = msg.GetPath()
            self.path = path
            
            if not self.player.Load(path):
                wx.MessageBox("Unable to load this file, it is in the wrong format")
            else:
                self.player.Play()        

    def playFile(self, event):
        "Plays Chosen Media"
        self.player.Play()
        self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image2, size = (self.image2.GetWidth()+4, self.image2.GetHeight()+4), style=wx.NO_BORDER)
        self.play.Bind(wx.EVT_BUTTON, self.pauseFile)
        self.slider.SetRange(0, self.player.Length())
        #self.info_length.SetLabel('length: %d seconds' % (self.player.Length()/1000))
        #self.info_name.SetLabel("Name: %s" % (os.path.split(self.path)[1]))
        self.panel.SetInitialSize()
        self.SetInitialSize()
          

    def pauseFile(self,event):
	"pauses playing of file, callback for pause button"
        self.player.Pause()
        self.play = wx.BitmapButton(panel, id=-1, bitmap=selfimage1, size = (self.image1.GetWidth()+4, self.image1.GetHeight()+4), style=wx.NO_BORDER)
        self.play.Bind(wx.EVT_BUTTON, self.playFile)

    def Seek(self,event):
        "Seeks in slider"   
        self.player.Seek(self.slider.GetValue())

    def splitFile():
        "takes a segment of the audio from time t1 to t2"          


#
# Start of main program
#


app = wx.App(False)
frame = TestToolBar(parent=None)
app.MainLoop()
