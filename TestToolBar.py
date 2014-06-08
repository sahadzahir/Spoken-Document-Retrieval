# !/usr/bin/python
"""
Authors: Sahad, Shashvat
Last updated:    Thu, May 22, 2014  5:06:55 PM
"""

import wx
import images
import wx.media
import wave
import wx.lib.scrolledpanel as scrolled
# from pydub import AudioSegment

FRAMETB = True
TBFLAGS = ( wx.TB_HORIZONTAL  # toolbar arranges icons horizontally
            | wx.NO_BORDER  # don't show borders
            | wx.TB_FLAT  #
            #| wx.TB_TEXT			    # 
            #| wx.TB_HORZ_LAYOUT			
)

# Array of 'Play' Bitmap Buttons
Play_Array = []

#Array of sliders
Slider_Array = []

#Keeps track of the number of sliders
numberOfSliders = 0
#---------------------------------------------------------------------------


class TestToolBar(wx.Frame):
    "Creates UI for Program"

    query = ""


    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Test ToolBar', size=(600, 400))


        self.panel = scrolled.ScrolledPanel(self, -1, size=(350, 50),
                                            style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER, name="panel")
        self.player = wx.media.MediaCtrl(self.panel)
        self.sizer = wx.FlexGridSizer(cols=3, vgap=20, hgap=1)


        # Play Button Image converted to Bitmap
        imageFile = "images/button_play.png"
        self.image1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        # Pause Button Image converted to Bitmap
        imageFile2 = "images/button_pause.png"
        self.image2 = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        # Search Button Image converted to Bitmap
        imageFile3 = "images/button_search.png"
        self.image3 = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()


        #Creates the main slider and play button
        self.mainPlay = wx.BitmapButton(self.panel, id=-1, bitmap=self.image1,
                                        size=(self.image1.GetWidth() + 4, self.image1.GetHeight() + 4),
                                        style=wx.NO_BORDER, name = "0")
        self.mainPlay.Bind(wx.EVT_BUTTON, self.playFile)
        Play_Array.append(self.mainPlay)
        self.sizer.Add(self.mainPlay, wx.ALIGN_RIGHT | wx.RIGHT)
        self.mainSlider = wx.Slider(self.panel, wx.ID_ANY, size=(300, -1))
        self.mainSlider.Bind(wx.EVT_SLIDER, self.Seek)
        self.mainSlider.Disable()
        Slider_Array.append(self.mainSlider)
        self.sizer.Add(self.mainSlider)
        self.mainTime = wx.StaticText(self.panel, label="0:00")
        self.sizer.Add(self.mainTime)

        blank_1 = wx.StaticText(self.panel, size=(100, 1))
        self.sizer.Add(blank_1)

        #Search Bar to receive input through enter/return 
        self.searchBar = wx.SearchCtrl(self.panel, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.searchBar.ShowCancelButton(True)
        self.searchBar.ShowSearchButton(True)
        self.searchBar.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onSearch, self.searchBar)
        self.sizer.Add(self.searchBar, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

        blank_3 = wx.StaticText(self.panel, size=(170, 1))
        self.sizer.Add(blank_3)

        font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'Segoe UI SemiLight')
        text1 = wx.StaticText(self.panel, label="Search Results")
        text1.SetFont(font)
        self.sizer.Add(text1, wx.ALIGN_CENTER_HORIZONTAL)

        blank2 = wx.StaticText(self.panel, size=(100, 1))
        self.sizer.Add(blank2)
        blank3 = wx.StaticText(self.panel, size=(100, 1))
        self.sizer.Add(blank3)

        # Separator Lines
        line3 = wx.StaticLine(self.panel)
        line4 = wx.StaticLine(self.panel)
        line5 = wx.StaticLine(self.panel)
        self.sizer.Add(line3, flag=wx.EXPAND)
        self.sizer.Add(line4, flag=wx.EXPAND)
        self.sizer.Add(line5, flag=wx.EXPAND)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(10)

        #Creates sliders and their buttons, argument is the number of sliders to create
        self.createSliders(2)

        self.panel.SetSizer(self.sizer)
        self.panel.SetAutoLayout(1)
        self.panel.SetupScrolling(scroll_x=False)

        if FRAMETB:
            tb = self.CreateToolBar(TBFLAGS)
        else:
            tb = wx.ToolBar(client, style=TBFLAGS)
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(tb, 0, wx.EXPAND)
            client.SetSizer(sizer)

        self.CreateStatusBar()

        tsize = (24, 24)
        new_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        history_bmp = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW,wx.ART_TOOLBAR,tsize)

        tb.SetToolBitmapSize(tsize)

        #tb.AddSimpleTool(10, open_bmp, "Open", "Long help for 'Open'")
        tb.AddLabelTool(10, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, self.openFile, id=10)
        recent = tb.AddLabelTool(11,"Recent",shortHelp= "Recent Files",bitmap = history_bmp,longHelp="Opens Recent Files")
        tb.AddSeparator()
        cbID = wx.NewId()

        tb.AddStretchableSpace()

        # Checks if file has been opened
        self.fileOpen = 0

        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        tb.Realize()
        self.Show()

    def openFile(self, event):
        "Opens File Dialog for choosing media file"
        msg = wx.FileDialog(self, message="Open a media file",
                            style=wx.OPEN,
                            wildcard="Media Files|*.wma;*.mp3;*.avi;*.wav")
        if msg.ShowModal() == wx.ID_OK:
            path = msg.GetPath()
            self.path = path

        if not self.player.Load(path):
            wx.MessageBox("Unable to load this file, it is in the wrong format")
        else:
            self.fileOpen = 1
            #self.playFile(self)
            for i in range(1,numberOfSliders+1):
                Slider_Array[i].Enable()
            self.mainSlider.Enable()


    def playFile(self, event):
        "Plays Chosen Media"
        if self.fileOpen == 0:
            filenotOpenMessageBox = wx.MessageDialog(None, 'Please choose a file first!', 'Error!', wx.ICON_ERROR)
            filenotOpenMessageBox.ShowModal()
        else:
            sourcenum = int(event.GetEventObject().GetName())
            source = Play_Array[sourcenum]
            source.SetBitmap(self.image2)
            self.player.Play()

            # self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image2,
            #                             size=(self.image2.GetWidth() + 4, self.image2.GetHeight() + 4),
            #                             style=wx.NO_BORDER)
            source.Bind(wx.EVT_BUTTON, self.pauseFile)
            Slider_Array[0].SetRange(0, self.player.Length())
            #self.info_length.SetLabel('length: %d seconds' % (self.player.Length()/1000))
            #self.info_name.SetLabel("Name: %s" % (os.path.split(self.path)[1]))


    def onTimer(self, event):
        "The timer for slider"
        current = self.player.Tell()

        if (current < 0):
            current = 0
        Slider_Array[0].SetValue(current)

        hours  = (current / 1000) / 3600
        minutes = (current / 1000) / 60 - (hours * 60)
        seconds = (current / 1000) - (minutes * 60) - (hours*3600)

        if (current == self.player.Length()):
            Slider_Array[0].SetValue(0)
            hours = 0
            minutes = 0
            seconds = 0

        #Doesnt display as 0:XX:XX when less than an hour has elapsed.
        if hours<=0:
            self.mainTime.SetLabel(' %d:%.2d ' % (minutes, seconds))
        else:
            self.mainTime.SetLabel(' %d:%.2d:%.2d ' %(hours,minutes,seconds))

    def onSearch(self, event):
        query = self.searchBar.GetValue()
        print query
        if not query == "":
            filenotOpenMessageBox = wx.MessageDialog(None, 'Please choose a file first!', 'Error!', wx.ICON_ERROR)
            filenotOpenMessageBox.ShowModal()


    def pauseFile(self, event):
        "pauses playing of file, callback for pause button"
        sourcenum = int(event.GetEventObject().GetName())
        source = Play_Array[sourcenum]
        self.player.Pause()
        #self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image1,size=(self.image1.GetWidth() + 4, self.image1.GetHeight() + 4), style=wx.NO_BORDER)
        source.SetBitmap(self.image1)
        source.Bind(wx.EVT_BUTTON, self.playFile)


    def Seek(self, event):
        "Seeks in slider"
        self.player.Seek(Slider_Array[0].GetValue())


    def splitAudio(a, b):
        "splits the audio file from t=a to t=b milliseconds"
        path = "/Users/CardMaster/Desktop/hi.wav"
        audio = AudioSegment.from_wav(
        "/Users/CardMaster/Dropbox/SMP 2014/background/time-frequency-lab/stimuli_lab/example5.wav")
        audio_segment = [100]
        audio_segment[0] = audio[:b]
        audio_segment[0].export(path, format="wav")
        audio = AudioSegment.from_wav(path)
        a = (len(audio) - a)
        audio_segment[0] = audio[a:]
        audio_segment[0].export(path, format="wav")  

    #DONT KNOW WHY THIS DOESNT WORK

    def createSliders(self,number):
        numberOfSliders.__add__(number)
        #for loop that creates sliders and play buttons
        for i in range(1,number+1):
            self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image1,
                                        size=(self.image1.GetWidth() + 4, self.image1.GetHeight() + 4),
                                        style=wx.NO_BORDER,
                                        name = str(i))
            self.play.Bind(wx.EVT_BUTTON, self.playFile)
            Play_Array.append(self.play)
            self.sizer.Add(self.play, wx.ALIGN_RIGHT | wx.RIGHT)
            slider = wx.Slider(self.panel, wx.ID_ANY, size=(300, -1))
            slider.Bind(wx.EVT_SLIDER, self.Seek)
            slider.Disable()
            Slider_Array.append(slider)
            self.sizer.Add(slider)
            blank_4 = wx.StaticText(self.panel, label="0:00")
            self.sizer.Add(blank_4)
            line_1 = wx.StaticLine(self.panel)
            line_2 = wx.StaticLine(self.panel)
            line_3 = wx.StaticLine(self.panel)
            self.sizer.Add(line_1, flag=wx.EXPAND)
            self.sizer.Add(line_2, flag=wx.EXPAND)
            self.sizer.Add(line_3, flag=wx.EXPAND)

#
# Start of main program
#


app = wx.App(False)
frame = TestToolBar(parent=None)
app.MainLoop()
