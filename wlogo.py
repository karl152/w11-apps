# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# SPDX-License-Identifier: MIT

import wx, wx.svg, platform, os

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

class WlogoFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wlogo", size=(250, 250))
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(5, 5)
        if platform.system() == "Windows":
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
        elif platform.system() == "Darwin":
            pass
        else:
            if os.environ.get("XDG_SESSION_TYPE") == "wayland":
                self.X11 = False
                self.SVGImage = wx.svg.SVGimage.CreateFromFile("Wayland.svg")
            elif os.environ.get("DISPLAY"):
                self.X11 = True
                self.SVGImage = wx.svg.SVGimage.CreateFromFile("X11.svg")
            else:
                self.X11 = False
                self.SVGImage = wx.svg.SVGimage.CreateFromFile("X11.svg")
            self.panel.Bind(wx.EVT_PAINT, self.draw)
            self.panel.Bind(wx.EVT_SIZE, lambda event: self.panel.Refresh())
        self.Show()
    def draw(self, event):
        self.PDC = wx.PaintDC(self.panel)
        if self.X11 == True:
            self.PDC.SetBackground(wx.Brush("#d22232"))
            self.PDC.Clear()
        self.GC = wx.GraphicsContext.Create(self.PDC)
        WWidth, WHeight = self.panel.GetClientSize()
        SVGWidth = self.SVGImage.width
        SVGHeight = self.SVGImage.height
        Scale = min(WWidth/SVGWidth, WHeight/SVGHeight)
        X = (WWidth - SVGWidth * Scale) / 2
        Y = (WHeight - SVGHeight * Scale) / 2
        self.GC.Translate(X, Y)
        self.GC.Scale(Scale, Scale)
        self.SVGImage.RenderToGC(self.GC)

app = wx.App()
frame = WlogoFrame()
frame.Show()
app.MainLoop()
