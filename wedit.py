# Copyright (C) 2026 karl152
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import tkinter as tk
from tkinter import ttk, filedialog
import sys

QuitQuestion = True
FilePath = ""

def writeToConsole(string):
    Console.configure(state="normal")
    Console.insert(tk.END, string + "\n")
    Console.configure(state="disabled")
def updateLineNumber():
    LN = str(TextBox.index("insert").split(".")[0])
    Linenumber.config(text="L" + LN)
    Window.after(200, updateLineNumber)
def close():
    global QuitQuestion
    if QuitQuestion == True:
        QuitQuestion = False
        writeToConsole("Click again to quit.")
    else:
        Window.destroy()
def save():
    if PathInput.get() == "":
        file = filedialog.asksaveasfilename(parent=Window)
    else:
        file = PathInput.get()
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(TextBox.get(1.0, tk.END).rstrip())
        Status.config(text=file)
        PathInputText.set(value=file)
    except:
        writeToConsole("Couln't save " + file)
    TextBox.focus_set()
def load():
    if PathInput.get() == "":
        file = filedialog.askopenfilename(parent=Window)
    else:
        file = PathInput.get()
    try:
        with open(file, "r", encoding="utf-8") as FileContent:
            TextBox.delete(1.0, tk.END)
            for line in FileContent:
                TextBox.insert(tk.END, line)
        Status.config(text=file)
        PathInputText.set(value=file)
    except:
        writeToConsole("Couln't open " + file)
    TextBox.focus_set()
def loadfile(file):
    try:
        with open(file, "r", encoding="utf-8") as FileContent:
            TextBox.delete(1.0, tk.END)
            for line in FileContent:
                TextBox.insert(tk.END, line)
        Status.config(text=file)
        PathInputText.set(value=file)
    except:
        writeToConsole("Couln't open " + file)
    TextBox.focus_set()

Window = tk.Tk()
PathInputText = tk.StringVar()
Window.title("Wedit")
Window.rowconfigure(8, weight=1)
Window.columnconfigure(4, weight=1)
ttk.Button(Window, text="Quit", command=close).grid(row=0, column=0, columnspan=2)
ttk.Button(Window, text="Save", command=save).grid(row=0, column=2)
ttk.Button(Window, text="Load", command=load).grid(row=0, column=3)
PathInput = ttk.Entry(Window, textvariable=PathInputText)
PathInput.grid(row=0, column=4, columnspan=2, sticky="ew")
SeparatorRows = [1, 3, 5, 7]
for row in SeparatorRows:
    ttk.Separator(Window, orient="horizontal").grid(row=row, column=0, columnspan=6, sticky="ew")
ttk.Label(Window, text="Use Control-S and Control-R to Search.").grid(row=2, column=0, columnspan=5)
Console = tk.Text(Window, height=3, state="disabled")
Console.grid(row=4, column=0, columnspan=6, sticky="ew")
Status = ttk.Label(Window, text="no file yet")
Status.grid(row=6, column=0, columnspan=5)
Linenumber = ttk.Label(Window, text="L1")
Linenumber.grid(row=6, column=5, sticky="e", padx=25)
ScrollBar = ttk.Scrollbar(Window, orient="vertical")
ScrollBar.grid(row=8, column=0, sticky="sn")
TextBox = tk.Text(Window, yscrollcommand=ScrollBar.set)
ScrollBar.config(command=TextBox.yview)
TextBox.grid(row=8, column=1, columnspan=5, sticky="news")
TextBox.focus_set()
if len(sys.argv) > 1:
    loadfile(sys.argv[1])
Window.after(512, updateLineNumber)
Window.mainloop()
