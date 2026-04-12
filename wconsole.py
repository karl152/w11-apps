import wx, argparse, platform

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

class WmoreFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wconsole")
        self.args = self.parseArgs()
        self.font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.panel = wx.Panel(self)
        self.Text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.Text.SetFont(self.font)
        self.sizer = wx.GridBagSizer(1, 1)
        self.sizer.AddGrowableCol(0)
        self.sizer.AddGrowableRow(0)
        self.sizer.Add(self.Text, pos=(0, 0), flag=wx.EXPAND)
        self.panel.SetSizer(self.sizer)
        self.loadFile("")
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.loadFile, self.timer)
        self.timer.Start(1000)
        self.Text.SetEditable(False)
    def loadFile(self, event):
        try:
            with open(self.args.file, "r", encoding="utf-8") as file:
                log = file.read()
                if self.args.saveLines:
                    lines = log.splitlines()
                    lines = lines[-self.args.saveLines:]
                    log = "\n".join(lines)
                self.Text.SetValue(log)
                    
            self.Text.ShowPosition(self.Text.GetLastPosition())
        except:
            self.Text.SetValue("Couldn't open console")
            if self.args.exitOnFail:
                self.Close()
        try:
            event.Skip()
        except:
            pass
    def parseArgs(self):
        parser = argparse.ArgumentParser(prog="wconsole")
        parser.add_argument("-file", type=str, help="file to read from")
        parser.add_argument("-exitOnFail", action="store_true", help="exit when unable to read")
        parser.add_argument("-saveLines", type=int, help='only preserve x lines of message history')
        return parser.parse_args()

app = wx.App()
frame = WmoreFrame()
frame.Show()
app.MainLoop()
