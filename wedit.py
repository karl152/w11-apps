# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import wx, sys
from wx import stc

class myFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Wedit")
        self.DontCheckIfSaved = False
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        panel = wx.Panel(self)
        QuitButton = wx.Button(panel, label="Quit")
        SaveButton = wx.Button(panel, label="Save")
        LoadButton = wx.Button(panel, label="Load")
        QuitButton.Bind(wx.EVT_BUTTON, lambda event: self.Close() if self.checkIfSaved(self.PathEntry.GetValue(), self.TextArea.GetText()) == True else self.SetDontCheckIfSaved(True))
        SaveButton.Bind(wx.EVT_BUTTON, lambda event: self.save(self.TextArea.GetText()) if self.PathEntry.GetValue() == "" else self.savefile(self.PathEntry.GetValue(), self.TextArea.GetText()))
        LoadButton.Bind(wx.EVT_BUTTON, lambda event: self.load() if self.PathEntry.GetValue() == "" else self.loadfile(self.PathEntry.GetValue()))
        self.PathEntry = wx.TextCtrl(panel)
        InfoText = wx.StaticText(panel, label="Use Control-S and Control-R to Search.")
        self.Splitter = wx.SplitterWindow(panel)
        self.TopPanel = wx.Panel(self.Splitter)
        self.BottomPanel = wx.Panel(self.Splitter)
        self.TopSizer = wx.GridBagSizer(1, 1)
        self.BottomSizer = wx.GridBagSizer(2, 2)
        self.TopPanel.SetSizer(self.TopSizer)
        self.BottomPanel.SetSizer(self.BottomSizer)
        self.Console = wx.TextCtrl(self.TopPanel, style=wx.TE_MULTILINE)
        self.Console.SetFont(font)
        self.PathText = wx.StaticText(self.BottomPanel, label="no file yet")
        self.LineThing = wx.StaticText(self.BottomPanel, label="L1")
        self.TextArea = stc.StyledTextCtrl(self.BottomPanel, style=wx.TE_MULTILINE)
        self.TextArea.StyleSetFont(stc.STC_STYLE_DEFAULT, font)
        self.TextArea.Bind(stc.EVT_STC_UPDATEUI, self.updateLineNumber)
        sizer = wx.GridBagSizer(3, 4)
        sizer.Add(QuitButton, pos=(0, 0))
        sizer.Add(SaveButton, pos=(0, 1))
        sizer.Add(LoadButton, pos=(0, 2))
        sizer.Add(self.PathEntry, pos=(0, 3), flag=wx.EXPAND)
        sizer.Add(InfoText, pos=(1, 0), span=(1, 4), flag=wx.ALIGN_CENTER)
        sizer.Add(self.Splitter, pos=(2, 0), span=(1, 4), flag=wx.EXPAND)
        self.TopSizer.Add(self.Console, pos=(0, 0), flag=wx.EXPAND)
        self.BottomSizer.Add(self.PathText, pos=(0, 0), flag=wx.ALIGN_CENTER)
        self.BottomSizer.Add(self.LineThing, pos=(0, 1), flag=wx.ALIGN_CENTER)
        self.BottomSizer.Add(self.TextArea, pos=(1, 0), span=(1, 2), flag=wx.EXPAND)
        self.Splitter.SplitHorizontally(self.TopPanel, self.BottomPanel, 40)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(2)
        self.TopSizer.AddGrowableCol(0)
        self.TopSizer.AddGrowableRow(0)
        self.BottomSizer.AddGrowableCol(0)
        self.BottomSizer.AddGrowableRow(1)
        panel.SetSizer(sizer)
        self.TextArea.SetFocus()
    def save(self, content):
        with wx.FileDialog(self, "Save file", style=wx.FD_SAVE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.PathEntry.SetValue(path)
                self.PathText.SetLabel(path)
                self.BottomPanel.Layout()
                self.savefile(path, content)
    def savefile(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content.rstrip())
                self.SetDontCheckIfSaved(False)
        except:
            self.Console.AppendText(f"Couldn't save {path}\n")
        self.TextArea.SetFocus()
    def load(self):
        with wx.FileDialog(self, "Load file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.PathEntry.SetValue(path)
                self.PathText.SetLabel(path)
                self.BottomPanel.Layout()
                self.loadfile(path)
    def loadfile(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.TextArea.SetText(file.read())
        except:
            pass
        self.PathEntry.SetValue(path)
        self.PathText.SetLabel(path)
        self.BottomPanel.Layout()
        self.TextArea.SetFocus()
    def updateLineNumber(self, event):
        LineNumber = self.TextArea.GetCurrentLine()
        self.LineThing.SetLabel(f"L{LineNumber+1}")
        self.BottomPanel.Layout()
        self.SetDontCheckIfSaved(False)
        event.Skip()
    def checkIfSaved(self, path, content):
        if self.DontCheckIfSaved == True:
            return True
        else:
            if path == "":
                if content == "":
                    return True
                else:
                    self.Console.AppendText(f"Unsaved changes. Save them, or Quit again.\n")
                    return False
            else:
                with open(path, "r", encoding="utf-8") as file:
                    if file.read().rstrip() == content.rstrip():
                        return True
                    else:
                        self.Console.AppendText(f"Unsaved changes. Save them, or Quit again.\n")
                        return False
    def SetDontCheckIfSaved(self, value):
        self.DontCheckIfSaved = value

app = wx.App()
frame = myFrame()
if len(sys.argv) > 1:
    frame.loadfile(sys.argv[1])
frame.Show()
app.MainLoop()
