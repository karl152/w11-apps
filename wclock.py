# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# SPDX-License-Identifier: MIT

import wx, wx.lib.analogclock, time, sys, platform
from datetime import datetime

if platform.system() == "Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

class WclockAnalogFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wclock", size=(200, 200))
        self.panel = wx.Panel(self)
        self.clock = wx.lib.analogclock.AnalogClock(self.panel)
        self.sizer = wx.GridBagSizer(1, 1)
        self.sizer.AddGrowableRow(0)
        self.sizer.AddGrowableCol(0)
        self.sizer.Add(self.clock, pos=(0, 0), flag=wx.EXPAND | wx.ALL)
        self.panel.SetSizer(self.sizer)
class WclockDigitalFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wclock")
        self.WeekDayThing = {
            "1": "Mon",
            "2": "Tue",
            "3": "Wed",
            "4": "Thu",
            "5": "Fri",
            "6": "Sat",
            "7": "Sun"}
        self.MonthThing = {
            "1": "Jan",
            "2": "Feb",
            "3": "Mar",
            "4": "Apr",
            "5": "May",
            "6": "Jun",
            "7": "Jul",
            "8": "Aug",
            "9": "Sep"}
        self.panel = wx.Panel(self)
        self.clock = wx.StaticText(self.panel, label="")
        self.clock.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.spacer = wx.StaticText(self.panel, label="\n")
        self.updateDisplay()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, lambda event: self.updateDisplay())
        self.timer.Start(1000)
        self.sizer = wx.GridBagSizer(1, 1)
        self.sizer.Add(self.clock, pos=(0, 0), flag=wx.ALL, border=5)
        self.sizer.Add(self.spacer, pos=(1, 0))
        self.panel.SetSizer(self.sizer)
        self.panel.Fit()
        self.Fit()
    def updateDisplay(self):
        now = datetime.now()
        isoweekday = str(now.isoweekday())
        weekday = isoweekday.translate(str.maketrans(self.WeekDayThing))
        day = now.day
        month = str(now.month).translate(str.maketrans(self.MonthThing)).replace("10", "Oct").replace("11", "Nov").replace("12", "Dec")
        year = now.year
        currenttime = str(datetime.now().time())[:8]
        if time.daylight == 1:
            timezone = time.tzname[1]
        else:
            timezone = time.tzname[0]
        self.clock.SetLabel(f"{weekday} {day} {month} {year} {currenttime} {timezone}")

if "-h" in sys.argv or "-help" in sys.argv or "--help" in sys.argv or "/?" in sys.argv:
    print("Usage: wclock [-analog] [-digital]")
else:
    app = wx.App()
    if not "-digital" in sys.argv:
        frame = WclockAnalogFrame()
    else:
        frame = WclockDigitalFrame()
    frame.Show()
    app.MainLoop()
