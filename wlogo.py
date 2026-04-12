# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# SPDX-License-Identifier: MIT

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
