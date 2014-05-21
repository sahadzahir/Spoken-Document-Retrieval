import  wx
import  images

FRAMETB = True
TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            #| wx.TB_TEXT
            #| wx.TB_HORZ_LAYOUT
            )

#---------------------------------------------------------------------------
    


class Newt(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, -1, title, size=(550, 500))

        box = wx.BoxSizer(wx.VERTICAL)
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        quit = wx.MenuItem(menu, ID_QUIT, '&Quit\tCtrl+Q', 'Quits Newt')
        quit.SetBitmap(wx.Bitmap('icons/exit16.png'))
        menu.AppendItem(quit)
        menuBar.Append(menu, '&File')
        self.Bind(wx.EVT_MENU, self.OnQuitNewt, id=ID_QUIT)
        self.SetMenuBar(menuBar)


        self.toolbar = wx.ToolBar(self, id=-1, style=wx.TB_HORIZONTAL | wx.NO_BORDER |
                                        wx.TB_FLAT | wx.TB_TEXT)
        self.toolbar.AddSimpleTool(ID_UNDO, wx.Bitmap('icons/undo.png'),
              'Undo', '')
        self.toolbar.AddSimpleTool(ID_REDO, wx.Bitmap('icons/redo.png'),
              'Redo', '')
        self.toolbar.EnableTool(ID_UNDO, False)

        self.toolbar.EnableTool(ID_REDO, False)
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(ID_EXIT, wx.Bitmap('icons/exit.png'),
              'Quit', '')
        self.toolbar.Realize()
        self.toolbar.Bind(wx.EVT_TOOL, self.OnUndo, id=ID_UNDO)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnRedo, id=ID_REDO)
        self.toolbar.Bind(wx.EVT_TOOL, self.OnQuitNewt, id=ID_EXIT)

        box.Add(self.toolbar, border=5)
        box.Add((5,10), 0)

        self.SetSizer(box)
        self.sheet1 = MySheet(self)
        self.sheet1.SetNumberRows(55)
        self.sheet1.SetNumberCols(25)




    def DoSearch(self,  text):
        # called by TestSearchCtrl
        # return true to tell the search ctrl to remember the text
        return True
    

    def OnToolClick(self, event):
        #tb = self.GetToolBar()
        tb = event.GetEventObject()
        tb.EnableTool(10, not tb.GetToolEnabled(10))

    def OpenFile(self, event):
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

    def OnToolRClick(self, event):
        pass

    def OnCombo(self, event):
        pass

    def OnToolEnter(self, event):

        if self.timer is None:
            self.timer = wx.Timer(self)

        if self.timer.IsRunning():
            self.timer.Stop()

        self.timer.Start(2000)
        event.Skip()


    def OnClearSB(self, event):  # called for the timer event handler
        self.SetStatusText("")
        self.timer.Stop()
        self.timer = None


    def OnCloseWindow(self, event):
        if self.timer is not None:
            self.timer.Stop()
            self.timer = None
        self.Destroy()

app = wx.App(False)
frame = New(None, -1, 'Newt')
app.MainLoop()