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
import Lattice
from pydub import AudioSegment

FRAMETB = True
TBFLAGS = ( wx.TB_HORIZONTAL  # toolbar arranges icons horizontally
            | wx.NO_BORDER  # don't show borders
            | wx.TB_FLAT  #
           )

# Array of 'Play' Bitmap Buttons
Play_Array = []

#Array of sliders
Slider_Array = []

#---------------------------------------------------------------------------

lecture = None

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
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
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
        frame = PopUp(self)
        frame.Show()

    def playFile(self, event):
        "Plays Chosen Media"
        if self.fileOpen == 0:
            filenotOpenMessageBox = wx.MessageDialog(None, 'Please choose a file first!', 'Error!', wx.ICON_ERROR)
            filenotOpenMessageBox.ShowModal()
        else:
            sourcenum = int(event.GetEventObject().GetName())
            source = Play_Array[sourcenum]
            source.SetBitmap(self.image2)
            source.Bind(wx.EVT_BUTTON, self.pauseFile)

            if sourcenum == 0:
                self.player.Play()
                Slider_Array[0].SetRange(0, self.player.Length())
                #self.info_length.SetLabel('length: %d seconds' % (self.player.Length()/1000))
                #self.info_name.SetLabel("Name: %s" % (os.path.split(self.path)[1]))

    def onTimer(self, event):
        "The timer for slider"
        current = self.player.Tell()

        if (current < 0):
            current = 0
        Slider_Array[0].SetValue(current)

        if(current == self.player.Length()):
            Play_Array[0].SetBitmap(self.image1)

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
        # print query
        # if not query == "":
        #     filenotOpenMessageBox = wx.MessageDialog(None, 'Please choose a file first!', 'Error!', wx.ICON_ERROR)
        #     filenotOpenMessageBox.ShowModal()


        #lattice = lecture.getLattice()            This is what the actual code should be like

        lattice = Lattice.Lattice()             # This is just
        lattice.parseFile("lattice.txt")        # for testing
        if lattice.getInvertedIndex().has_key(query):
            self.createSliders(len(lattice.getInvertedIndex()[query]))


    def pauseFile(self, event):
        "pauses playing of file, callback for pause button"
        sourcenum = int(event.GetEventObject().GetName())
        source = Play_Array[sourcenum]
        source.SetBitmap(self.image1)
        source.Bind(wx.EVT_BUTTON, self.playFile)

        if sourcenum==0:
            self.player.Pause()

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

    def createSliders(self,number):
        for p in range (len(Slider_Array)):
            Slider_Array[p].Destroy()
            Play_Array[p].Destroy()


        #for loop that creates sliders and play buttons
        for i in range(1,number+1):
            self.play = wx.BitmapButton(self.panel, id=-1, bitmap=self.image1,
                                        size=(self.image1.GetWidth() + 4, self.image1.GetHeight() + 4),
                                        style=wx.NO_BORDER,
                                        name = str(i),
                                        pos=(20,170+i*50)
            )

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

    def getPlayer(self):
        return self.player

##########################################################################################
import Lecture
class PopUp(wx.Frame):
    def __init__(self, myToolBar):
        self.myToolBar = myToolBar
        wx.Frame.__init__(self, None, title="Info", size=(490,250))
        self.panel = wx.Panel(self)
        self.sizer = wx.FlexGridSizer(cols=3, vgap=15, hgap=3)
        self.lbl1 = wx.StaticText(self.panel, -1, label="Audio Path: ")
        self.txtctrl1 = wx.TextCtrl(self.panel, -1, size=(300,25))
        self.browseBtn = wx.Button(self.panel, label="Browse")
        self.browseBtn.Bind(wx.EVT_BUTTON, self.browseFile)

        self.lbl2 = wx.StaticText(self.panel, -1, label="Date: ")
        self.txtctrl2 = wx.TextCtrl(self.panel, -1, size=(300,25))
        self.blank1 = wx.StaticText(self.panel, -1, label="")

        self.lbl3 = wx.StaticText(self.panel, -1, label="Gender: ")
        self.cb1 = wx.ComboBox(self.panel,choices=["Male", "Female"])
        self.blank2 = wx.StaticText(self.panel, -1, label="")

        self.lbl4 = wx.StaticText(self.panel, -1, label="Topic: ")
        self.txtctrl4 = wx.TextCtrl(self.panel, -1, size=(300,25))
        self.blank3 = wx.StaticText(self.panel, -1, label="")

        self.lbl5 = wx.StaticText(self.panel, -1, label="Subject: ")
        self.txtctrl5 = wx.TextCtrl(self.panel, -1, size=(300,25))
        self.blank4 = wx.StaticText(self.panel, -1, label="")

        self.blank5 = wx.StaticText(self.panel, -1, label="")
        self.okBtn = wx.Button(self.panel, label="Ok")
        self.okBtn.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.blank6 = wx.StaticText(self.panel, -1, label="")

        self.sizer.Add(self.lbl1)
        self.sizer.Add(self.txtctrl1)
        self.sizer.Add(self.browseBtn)
        self.sizer.Add(self.lbl2)
        self.sizer.Add(self.txtctrl2)
        self.sizer.Add(self.blank1)
        self.sizer.Add(self.lbl4)
        self.sizer.Add(self.txtctrl4)
        self.sizer.Add(self.blank3)
        self.sizer.Add(self.lbl5)
        self.sizer.Add(self.txtctrl5)
        self.sizer.Add(self.blank4)
        self.sizer.Add(self.lbl3)
        self.sizer.Add(self.cb1)
        self.sizer.Add(self.blank2)
        self.sizer.Add(self.blank5)
        self.sizer.Add(self.okBtn)
        self.sizer.Add(self.blank6)
        self.panel.SetSizer(self.sizer)

    def browseFile(self, event):

        msg = wx.FileDialog(self, message="Open a media file",
                           style=wx.OPEN,
                           wildcard="Media Files|*.wma;*.mp3;*.avi;*.wav")
        if msg.ShowModal() == wx.ID_OK:
            if not msg.GetPath == '' :
                path = msg.GetPath()
                self.path = path
                self.txtctrl1.SetValue(path)

                if not self.myToolBar.player.Load(path):
                    wx.MessageBox("Unable to load this file, it is in the wrong format")
                else:
                    self.myToolBar.fileOpen = 1
                    for i in range(1,numberOfSliders+1):
                        Slider_Array[i].Enable()
                    self.myToolBar.mainSlider.Enable()

    def onSubmit(self, event):
        if(self.txtctrl1.GetValue() == '' or self.txtctrl2.GetValue() == '' or self.txtctrl4.GetValue() == '' or self.txtctrl5.GetValue() == ''):
            fillBlanksMessageBox = wx.MessageDialog(None, 'Please fill in all blanks!', 'Error!', wx.ICON_ERROR)
            fillBlanksMessageBox.ShowModal()
        else:
            self.lecture = Lecture.Lecture()
            self.lecture.setFilePath(self.txtctrl1.GetValue())
            self.lecture.setDate(self.txtctrl2.GetValue())
            self.lecture.setGender(self.cb1.GetValue())
            self.lecture.setTopic(self.txtctrl4.GetValue())
            self.lecture.setSubject(self.txtctrl5.GetValue())
            self.Destroy()







#
# Start of main program
#

app = wx.App(False)
frame = TestToolBar(parent=None)
app.MainLoop()
