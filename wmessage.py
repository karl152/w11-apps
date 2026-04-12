import wx, sys, argparse, platform

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

class WmessageDialog(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="wmessage", style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.args = self.parseArgs()
        self.font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.panel = wx.Panel(self)
        self.Text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.Text.SetFont(self.font)
        if not self.args.buttons:
            self.sizer = wx.GridBagSizer(2, 1)
            self.sizer.AddGrowableCol(0)
        else:
            self.sizer = wx.GridBagSizer(2, len(self.args.buttons.split(",")))
        self.sizer.AddGrowableRow(0)
        if self.args.buttons:
            self.sizer.Add(self.Text, pos=(0, 0), span=(1, len(self.args.buttons.split(","))), flag=wx.EXPAND | wx.ALL, border=5)
        else:
            self.sizer.Add(self.Text, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=5)
        self.loadButtons()
        if self.args.default:
            self.HighlightedButton.SetDefault()
        self.panel.SetSizer(self.sizer)
        self.Text.SetValue(self.loadText())
        self.Text.SetEditable(False)
        if self.args.timeout:
            self.Timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.closeOnTimeout, self.Timer)
            self.Timer.Start(self.args.timeout * 1000, oneShot=True)
        self.Bind(wx.EVT_CLOSE, self.closeOnClose)
        self.sizer.Fit(self)
    def loadText(self):
        if not self.args.file:
            return self.args.message
        else:
            with open(self.args.file, "r", encoding="utf-8") as file:
                return(file.read())
    def loadButtons(self):
        if self.args.buttons:
            buttons = self.args.buttons.split(",")
            for index, button in enumerate(buttons):
                if ":" in button:
                    thebutton = button.split(":")[0]
                    exitcode = int(button.split(":")[1])
                else:
                    thebutton = button
                    exitcode = 0
                TmpButton = wx.Button(self.panel, label=thebutton)
                if self.args.default == thebutton:
                    self.HighlightedButton = TmpButton
                TmpButton.Bind(wx.EVT_BUTTON, lambda event, b=thebutton: self.closeOnButton(event, b, exitcode))
                self.sizer.Add(TmpButton, pos=(1, index), flag=wx.ALL, border=5)
            self.sizer.AddGrowableCol(len(self.args.buttons.split(","))-1)
        else:
            self.DefaultButton = wx.Button(self.panel, label="okay")
            if self.args.default == "okay":
                self.HighlightedButton = self.DefaultButton
            self.DefaultButton.Bind(wx.EVT_BUTTON, lambda event: self.closeOnButton(event, "okay", 0))
            self.sizer.Add(self.DefaultButton, pos=(1, 0), flag=wx.ALL, border=5)
    def closeOnButton(self, event, button, exitcode):
        if self.args.print:
            print(button)
        self.Close()
        event.Skip()
        sys.exit(exitcode)
    def closeOnClose(self, event):
        self.Close()
        event.Skip()
        sys.exit(0)
    def closeOnTimeout(self, event):
        self.Close()
        event.Skip()
        sys.exit(0)
    def parseArgs(self):
        parser = argparse.ArgumentParser(prog="wmessage")
        parser.add_argument("message", type=str)
        parser.add_argument("-file", type=str, help='file to read message from, "-" for stdin')
        parser.add_argument("-buttons", type=str, help="comma-separated list of label:exitcode")
        parser.add_argument("-default", type=str, help="button to activate if Return is pressed")
        parser.add_argument("-print", action="store_true", help="print the button label when selected")
        parser.add_argument("-timeout", type=int, help='exit with status 0 after "secs" seconds')
        return parser.parse_args()

app = wx.App()
frame = WmessageDialog()
frame.Show()
app.MainLoop()
