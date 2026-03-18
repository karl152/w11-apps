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
        QuitButton.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        SaveButton.Bind(wx.EVT_BUTTON, lambda event: self.save(self.TextArea.GetValue()) if self.PathEntry.GetValue() == "" else self.savefile(self.PathEntry.GetValue(), self.TextArea.GetValue()))
        LoadButton.Bind(wx.EVT_BUTTON, lambda event: self.load() if self.PathEntry.GetValue() == "" else self.loadfile(self.PathEntry.GetValue()))
        self.PathEntry = wx.TextCtrl(panel)
        InfoText = wx.StaticText(panel, label="Use Control-S and Control-R to Search.")
        self.Console = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.PathText = wx.StaticText(panel, label="no file yet")
        self.LineThing = wx.StaticText(panel, label="L1")
        self.TextArea = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.TextArea.Bind(wx.EVT_KEY_UP, self.updateLineNumber)
        self.TextArea.Bind(wx.EVT_LEFT_UP, self.updateLineNumber)
        sizer = wx.GridBagSizer(4, 5)
        sizer.Add(QuitButton, pos=(0, 0))
        sizer.Add(SaveButton, pos=(0, 1))
        sizer.Add(LoadButton, pos=(0, 2))
        sizer.Add(self.PathEntry, pos=(0, 3), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(InfoText, pos=(1, 0), span=(1, 5), flag=wx.ALIGN_CENTER)
        sizer.Add(self.Console, pos=(2, 0), span=(1, 5), flag=wx.EXPAND)
        sizer.Add(self.PathText, pos=(3, 0), span=(1, 4), flag=wx.ALIGN_CENTER)
        sizer.Add(self.LineThing, pos=(3, 4), flag=wx.ALIGN_CENTER)
        sizer.Add(self.TextArea, pos=(4, 0), span=(1, 5), flag=wx.EXPAND)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(4)
        panel.SetSizer(sizer)
    def save(self, content):
        with wx.FileDialog(self, "Save file", style=wx.FD_SAVE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.PathEntry.SetValue(path)
                self.PathText.SetLabel(path)
                self.savefile(path, content)
    def savefile(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content.rstrip())
        except:
            self.Console.AppendText(f"Couldn't save {path}\n")
    def load(self):
        with wx.FileDialog(self, "Load file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
                self.PathEntry.SetValue(path)
                self.PathText.SetLabel(path)
                self.loadfile(path)
    def loadfile(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.TextArea.SetValue(file.read())
        except:
            self.PathEntry.SetValue(path)
            self.PathText.SetLabel(path)
    def updateLineNumber(self, _):
        InsertionPoint = self.TextArea.GetInsertionPoint()
        LineNumber = len(self.TextArea.GetRange(0, InsertionPoint).split("\n"))
        self.LineThing.SetLabel(f"L{LineNumber}")

app = wx.App()
frame = myFrame()
frame.Show()
app.MainLoop()
