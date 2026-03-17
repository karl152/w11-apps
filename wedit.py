# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import wx

class myFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Wedit")
        panel = wx.Panel(self)
        QuitButton = wx.Button(panel, label="Quit")
        SaveButton = wx.Button(panel, label="Save")
        LoadButton = wx.Button(panel, label="Load")
        PathEntry = wx.TextCtrl(panel)
        InfoText = wx.StaticText(panel, label="Use Control-S and Control-R to Search.", style=wx.ALIGN_CENTER)
        Console = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        PathText = wx.StaticText(panel, label="no file yet", style=wx.ALIGN_CENTER)
        LineThing = wx.StaticText(panel, label="L1", style=wx.ALIGN_CENTER)
        TextArea = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer = wx.GridBagSizer(4, 6)
        sizer.Add(QuitButton, pos=(0, 0))
        sizer.Add(SaveButton, pos=(0, 1))
        sizer.Add(LoadButton, pos=(0, 2))
        sizer.Add(PathEntry, pos=(0, 3), span=(1, 3), flag=wx.EXPAND)
        sizer.Add(InfoText, pos=(1, 0), span=(1, 6), flag=wx.EXPAND)
        sizer.Add(Console, pos=(2, 0), span=(1, 6), flag=wx.EXPAND)
        sizer.Add(PathText, pos=(3, 0), span=(1, 3), flag=wx.EXPAND)
        sizer.Add(LineThing, pos=(3, 5))
        sizer.Add(TextArea, pos=(4, 0), span=(1, 6), flag=wx.EXPAND)
        sizer.AddGrowableCol(4)
        sizer.AddGrowableRow(4)
        panel.SetSizer(sizer)

app = wx.App()
frame = myFrame()
frame.Show()
app.MainLoop()
