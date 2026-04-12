import wx, platform

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

class WlogoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wlogo", size=(250, 250))
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(2, 2)
        for i in range(2):
            btn = wx.Button(self.panel, label="")
            btn.SetBackgroundColour("blue")
            btn.SetForegroundColour("blue")
            self.sizer.Add(btn, pos=(0, i), flag=wx.EXPAND | wx.ALL, border=2)
        for i in range(2):
            btn = wx.Button(self.panel, label="")
            btn.SetBackgroundColour("blue")
            btn.SetForegroundColour("blue")
            self.sizer.Add(btn, pos=(1, i), flag=wx.EXPAND | wx.ALL, border=2)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableRow(1)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableCol(1)
        self.panel.SetSizer(self.sizer)
        self.Show()

if platform.system() != "Windows":
    print("Your platform is currently not supported by Wlogo")
app = wx.App()
frame = WlogoFrame()
frame.Show()
app.MainLoop()
