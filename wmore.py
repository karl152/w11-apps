import wx, sys

class WmoreFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wmore", size=(700, 500))
        self.font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.panel = wx.Panel(self)
        self.Text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.Text.SetFont(self.font)
        self.QuitButton = wx.Button(self.panel, label="Quit")
        self.QuitButton.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        self.sizer = wx.GridBagSizer(2, 1)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.Add(self.Text, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=5)
        self.sizer.Add(self.QuitButton, pos=(1, 0), flag=wx.ALL, border=5)
        self.panel.SetSizer(self.sizer)
        self.loadFile()
        self.Text.SetEditable(False)
    def loadFile(self):
        if len(sys.argv) > 1:
            try:
                with open(sys.argv[1], "r", encoding="utf-8") as file:
                    self.Text.SetValue(file.read())
            except:
                print("Warning: Cannot open file " + sys.argv[1])

if len(sys.argv) < 2:
    print("usage: wmore <filename>")
else:
    app = wx.App()
    frame = WmoreFrame()
    frame.Show()
    app.MainLoop()
