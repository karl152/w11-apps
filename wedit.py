# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import wx, sys

class myFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Wedit")
        self.DontCheckIfSaved = False
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        panel = wx.Panel(self)
        QuitButton = wx.Button(panel, label="Quit")
        SaveButton = wx.Button(panel, label="Save")
        LoadButton = wx.Button(panel, label="Load")
        QuitButton.Bind(wx.EVT_BUTTON, lambda event: self.Close() if self.checkIfSaved(self.PathEntry.GetValue(), self.TextArea.GetValue()) == True else self.SetDontCheckIfSaved(True))
        SaveButton.Bind(wx.EVT_BUTTON, lambda event: self.save(self.TextArea.GetValue()) if self.PathEntry.GetValue() == "" else self.savefile(self.PathEntry.GetValue(), self.TextArea.GetValue()))
        LoadButton.Bind(wx.EVT_BUTTON, lambda event: self.load() if self.PathEntry.GetValue() == "" else self.loadfile(self.PathEntry.GetValue()))
        self.PathEntry = wx.TextCtrl(panel)
        InfoText = wx.StaticText(panel, label="Use Control-F and Control-R to Search.")
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
        self.TextArea = wx.TextCtrl(self.BottomPanel, style=wx.TE_MULTILINE)
        self.TextArea.SetFont(font)
        self.TextArea.Bind(wx.EVT_KEY_UP, self.updateLineNumber)
        self.TextArea.Bind(wx.EVT_LEFT_UP, self.updateLineNumber)
        self.TextArea.Bind(wx.EVT_KEY_DOWN, self.keyBind)
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
                self.TextArea.SetValue(file.read())
        except:
            pass
        self.PathEntry.SetValue(path)
        self.PathText.SetLabel(path)
        self.BottomPanel.Layout()
        self.TextArea.SetFocus()
    def updateLineNumber(self, event):
        InsertionPoint = self.TextArea.GetInsertionPoint()
        LineNumber = len(self.TextArea.GetRange(0, InsertionPoint).split("\n"))
        self.LineThing.SetLabel(f"L{LineNumber}")
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
    def keyBind(self, event):
        if event.ControlDown():
            if event.KeyCode == 70 or event.KeyCode == 82:
                SearchAndReplaceFrame(self)
        event.Skip()
class SearchAndReplaceFrame(wx.Dialog):
    def __init__(self, MainFrame):
        super().__init__(MainFrame, title="search")
        self.panel = wx.Panel(self)
        self.Description = wx.StaticText(self.panel, label="Use <Tab> to change fields.\nUse ^q<Tab> for <Tab>.")
        self.BackwardButton = wx.RadioButton(self.panel, label="Backward", style=wx.RB_GROUP)
        self.ForwardButton = wx.RadioButton(self.panel, label="Forward")
        self.CaseSensitiveCheckbox = wx.CheckBox(self.panel, label="Case Sensitive")
        self.CaseSensitiveCheckbox.SetValue(True)
        self.SearchForLabel = wx.StaticText(self.panel, label="Search for:")
        self.ReplaceWithLabel = wx.StaticText(self.panel, label="Replace with:")
        self.SearchEntry = wx.TextCtrl(self.panel)
        self.ReplaceEntry = wx.TextCtrl(self.panel)
        self.SearchButton = wx.Button(self.panel, label="Search")
        self.SearchButton.Bind(wx.EVT_BUTTON, lambda event: self.Search(MainFrame))
        self.ReplaceButton = wx.Button(self.panel, label="Replace")
        self.ReplaceButton.Bind(wx.EVT_BUTTON, lambda event: self.Replace(MainFrame))
        self.ReplaceAllButton = wx.Button(self.panel, label="Replace All")
        self.ReplaceAllButton.Bind(wx.EVT_BUTTON, lambda event: self.ReplaceAll(MainFrame))
        self.CancelButton = wx.Button(self.panel, label="Cancel")
        self.CancelButton.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        self.sizer = wx.GridBagSizer(5, 4)
        self.sizer.Add(self.Description, pos=(0, 0), span=(1, 4), flag=wx.ALL, border=10)
        self.sizer.Add(self.BackwardButton, pos=(1, 0), flag=wx.LEFT, border=5)
        self.sizer.Add(self.ForwardButton, pos=(1, 1))
        self.sizer.Add(self.CaseSensitiveCheckbox, pos=(1, 2), span=(1, 2), flag=wx.ALIGN_RIGHT | wx.RIGHT, border=5)
        self.sizer.Add(self.SearchForLabel, pos=(2, 0), flag=wx.LEFT, border=5)
        self.sizer.Add(self.ReplaceWithLabel, pos=(3, 0), flag=wx.LEFT, border=5)
        self.sizer.Add(self.SearchEntry, pos=(2, 1), span=(1, 3), flag=wx.EXPAND | wx.RIGHT, border=10)
        self.sizer.Add(self.ReplaceEntry, pos=(3, 1), span=(1, 3), flag=wx.EXPAND | wx.RIGHT, border=10)
        self.sizer.Add(self.SearchButton, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        self.sizer.Add(self.ReplaceButton, pos=(4, 1), flag=wx.BOTTOM, border=10)
        self.sizer.Add(self.ReplaceAllButton, pos=(4, 2), flag=wx.BOTTOM, border=10)
        self.sizer.Add(self.CancelButton, pos=(4, 3), flag=wx.RIGHT, border=25)
        self.panel.SetSizer(self.sizer)
        self.SearchEntry.SetFocus()
        self.panel.Fit()
        self.Fit()
        self.Show()
    def ReplaceAll(self, MainFrame):
        text = MainFrame.TextArea.GetValue()
        text = text.replace(self.SearchEntry.GetValue(), self.ReplaceEntry.GetValue())
        MainFrame.TextArea.SetValue(text)
    def Replace(self, MainFrame):
        searchtext = self.SearchEntry.GetValue()
        replacetext = self.ReplaceEntry.GetValue()
        if self.ForwardButton.GetValue() == True:
            position = MainFrame.TextArea.GetValue().find(searchtext)
        else:
            position = MainFrame.TextArea.GetValue().rfind(searchtext)
        if position != -1:
            MainFrame.TextArea.SetSelection(position, position+len(searchtext))
            MainFrame.TextArea.Replace(position, position+len(searchtext), replacetext)
        if self.ForwardButton.GetValue() == True:
            position = MainFrame.TextArea.GetValue().find(searchtext)
        else:
            position = MainFrame.TextArea.GetValue().rfind(searchtext)
        MainFrame.TextArea.SetFocus()
    def Search(self, MainFrame):
        searchtext = self.SearchEntry.GetValue()
        if self.ForwardButton.GetValue() == True:
            position = MainFrame.TextArea.GetValue().find(searchtext, MainFrame.TextArea.GetInsertionPoint())
        else:
            position = MainFrame.TextArea.GetValue().rfind(searchtext, 0, MainFrame.TextArea.GetInsertionPoint())
        if position != -1:
            MainFrame.TextArea.SetInsertionPoint(position + len(searchtext))
            if self.ForwardButton.GetValue() == True:
                MainFrame.TextArea.SetSelection(position+len(searchtext), position)
            else:
                MainFrame.TextArea.SetSelection(position, position+len(searchtext))
        MainFrame.TextArea.SetFocus()

app = wx.App()
frame = myFrame()
if len(sys.argv) > 1:
    frame.loadfile(sys.argv[1])
frame.Show()
app.MainLoop()
