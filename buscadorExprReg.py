# Luis Bodart  A01635000

from os import *
from os import path
from re import *
from tkinter import *
from tkinter import filedialog, messagebox


# window size & pos
def window(topFrame, width=800, height=500):
    topFrame.title("Buscador con Expresiones Regulares")
    topFrame.minsize(width, height)
    topFrame.maxsize(width, height)
    topFrame.resizable(False, False)
    screenW = topFrame.winfo_screenwidth()
    screenH = topFrame.winfo_screenheight()
    x = (screenW/2) - (width/2)
    y = (screenH/2.15) - (height/2)
    topFrame.geometry("%dx%d+%d+%d" % (width, height, x, y))

# start the App


class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.widgets()

    # create the widgets
    def widgets(self):
        self.dirLabel = Label(self, text="Directorio", width=100)
        self.dirLabel.grid(row=1, column=1, columnspan=5, sticky=W+E)

        self.dirScroll = Scrollbar(
            self, orient=HORIZONTAL, command=self.xScrollHandler)
        self.dirScroll.grid(row=3, column=1, columnspan=4, sticky=W+E)

        self.dirTxt = Entry(self, xscrollcommand=self.dirScroll.set)
        self.dirTxt.grid(row=2, column=1, columnspan=4, sticky=W+E)

        self.dirBtn = Button(
            self, text="Buscar Directorio", command=self.askDir)
        self.dirBtn.grid(row=2, column=5, columnspan=3, sticky=N+S+W+E)

        self.fileLabel = Label(self, text="Archivo")
        self.fileLabel.grid(row=4, column=1, columnspan=5, sticky=W+E)

        self.fileTxt = Entry(self)
        self.fileTxt.grid(row=5, column=1, columnspan=4, sticky=W+E)

        self.fileBtn = Button(self, text="Buscar Archivo",
                              command=self.askFiles)
        self.fileBtn.grid(row=5, column=5, columnspan=3, sticky=N+S+W+E)

        self.filesWindowName = PanedWindow(self, orient=VERTICAL)
        self.filesWindowName.grid(
            row=6, column=1, columnspan=2, sticky=N+S+W+E)

        self.filesWindowPath = PanedWindow(self, orient=VERTICAL)
        self.filesWindowPath.grid(
            row=6, column=3, columnspan=4, sticky=N+S+W+E)

        self.filesScroll = Scrollbar(
            self, orient=VERTICAL, command=self.yScrollHandler)
        self.filesScroll.grid(row=6, column=7, sticky=N+S)

        self.crateLists()

        self.filesWindowName.add(self.filesNameList)
        self.filesWindowName.add(self.filesScrollName)

        self.filesWindowPath.add(self.filesPathList)
        self.filesWindowPath.add(self.filesScrollPath)

    # make the horizontal scrollbar move
    def xScrollHandler(self, *A):
        move = A[1]
        if A[0] == "scroll":
            self.dirTxt.xview_scroll(move, UNITS)
        elif A[0] == "moveto":
            self.dirTxt.xview_moveto(move)

    # ask directory
    def askDir(self):
        directory = filedialog.askdirectory()
        if path.isdir(directory):
            self.dirTxt.delete(0, END)
            self.dirTxt.insert(0, directory)
        else:
            messagebox.showinfo(
                title="Directory Invalid", message="The given directory is invalid\nUsing default directory")
            self.dirTxt.delete(0, END)
            self.dirTxt.insert(0, getcwd())

    # search files with the name given
    def askFiles(self):
        directory = self.dirTxt.get()
        if path.isdir(directory):
            name = self.fileTxt.get()
            if self.validExpr(name):
                self.crateLists()
                f = 0
                for root, dirs, files in walk(directory):
                    for file in files:
                        i = 0
                        while i < len(self.characterList):
                            pattern = self.characterList[i]
                            if '*' in pattern and len(pattern) > 1:
                                for inside in pattern:
                                    if search(inside[i], file):
                                        self.fileData(file, root)
                                        f += 1
                            if pattern == '^':
                                i += 1
                                pattern = self.characterList[i]
                                if file.startswith(pattern):
                                    self.fileData(file, root)
                                    f += 1
                            elif pattern == '+':
                                i += 1
                                pattern = self.characterList[i]
                                if pattern == '^':
                                    i += 1
                                    pattern = self.characterList[i]
                                    if file.startswith(pattern):
                                        self.fileData(file, root)
                                        f += 1
                                else:
                                    if search(pattern, file):
                                        self.fileData(file, root)
                                        f += 1
                            elif pattern == '*':
                                pattern = self.characterList[i - 1]
                                if search(pattern, file):
                                    self.fileData(file, root)
                                    f += 1
                            else:
                                if search(pattern, file):
                                    self.fileData(file, root)
                                    f += 1
                            i += 1
                if f == 0:
                    messagebox.showerror(
                        title="No File Found", message="The given expression cannot match any file in the given directory")
            else:
                messagebox.showerror(title="Expression Invalid",
                                     message="The given expression is invalid")
        else:
            messagebox.showerror(title="Directory Invalid",
                                 message="The given directory is invalid")

    # check if the given expresion is valid '[A-Za-z0-9][(+*^)]'
    def validExpr(self, expr):
        if len(expr) == 0 or expr.isspace():
            return False
        exprStrip = expr.strip()
        if exprStrip != expr:
            return False
        if expr.isalnum():
            self.characterList = list(expr)
            return True
        hasAtStart = 0
        hasOpenP = 0
        hasClosedP = 0
        hasStar = 0
        hasPlus = 0
        # print(expr)
        for i in range(len(expr)):
            if i == '^':
                hasAtStart += 1
            if i == '(':
                hasOpenP += 1
            elif i == ')':
                hasClosedP += 1
            elif i == '*':
                hasStar += 1
            elif i == '+':
                hasPlus += 1
        if hasAtStart > 2:
            return False
        if hasPlus > 1:
            return False
        if hasOpenP != hasClosedP:
            return False
        self.characterList = list()
        ca = ''
        cs = ''
        i = 0
        s = ""
        insideP = False
        while i < len(expr):
            c = expr[i]
            if i > 0:
                ca = expr[i - 1]
            if i < len(expr) - 1:
                cs = expr[i + 1]
            else:
                cs = ''
            #print("ca {%s} c {%s} cs {%s}" % (ca, c, cs))
            if not c.isalnum():
                if c == '^':
                    if ca == '' or ca == '+':
                        if cs.isalnum():
                            i += 1
                            self.characterList.append(c)
                            self.characterList.append(cs)
                        elif cs == '(':
                            i += 2
                            insideP = True
                            self.characterList.append(c)
                            cs = expr[i]
                            if cs.isalnum():
                                s = cs
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                elif c == '(':
                    if (ca == '' or ca == '+' or ca.isalnum()) and (cs != ')' or cs.isalnum()):
                        i += 1
                        insideP = True
                        s = cs
                    else:
                        return False
                elif c == ')':
                    if (ca.isalnum() or ca == '*') and (cs == '' or cs == '*' or cs == '+' or cs.isalnum()):
                        insideP = False
                        self.characterList.append(s)
                    else:
                        return False
                elif c == '*':
                    if insideP:
                        s += c
                    else:
                        if ca == ')' or ca.isalnum():
                            if cs == '' or cs == '(' or cs == '+' or cs.isalnum():
                                self.characterList.append(c)
                            else:
                                self.characterList.append(ca)
                                self.characterList.append(c)
                        else:
                            return False
                elif c == '+':
                    if ca == '*' or ca == ')' or ca.isalnum():
                        if cs.isalnum():
                            i += 1
                            self.characterList.append(c)
                            self.characterList.append(cs)
                        elif cs == '^':
                            self.characterList.append(c)
                        elif cs == '(':
                            i += 2
                            insideP = True
                            self.characterList.append(c)
                            cs = expr[i]
                            if cs.isalnum():
                                s = cs
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                if insideP:
                    s += c
                else:
                    self.characterList.append(c)
            i += 1
        return True

    # create the lists that changes every time it search
    def crateLists(self):
        self.filesScrollName = Scrollbar(
            self.filesWindowName, orient=HORIZONTAL, command=self.xScrollName)
        self.filesScrollName.grid(row=1, column=0, sticky=W+E)

        self.filesScrollPath = Scrollbar(
            self.filesWindowPath, orient=HORIZONTAL, command=self.xScrollPath)
        self.filesScrollPath.grid(row=1, column=0, sticky=W+E)

        self.filesNameList = Listbox(
            self.filesWindowName, xscrollcommand=self.filesScrollName.set, yscrollcommand=self.yScrollName, width=32, height=22)
        self.filesNameList.grid(
            row=0, column=0, sticky=N+S+W+E)
        self.filesNameList.bind(
            '<<ListboxSelect>>', self.selectNameList)

        self.filesPathList = Listbox(
            self.filesWindowPath, xscrollcommand=self.filesScrollPath.set, yscrollcommand=self.yScrollPath, width=82, height=22)
        self.filesPathList.grid(
            row=0, column=0, sticky=N+S+W+E)
        self.filesPathList.bind(
            '<<ListboxSelect>>', self.selectPathList)

    # make the vertical scrollbar move both list
    def yScrollHandler(self, *A):
        self.filesNameList.yview(*A)
        self.filesPathList.yview(*A)

    # make the vertical path scrollbar move if names is moved
    def yScrollName(self, *A):
        move = A[1]
        if self.filesPathList.yview() != self.filesNameList.yview():
            self.filesPathList.yview_moveto(move)
        self.filesScroll.set(*A)

    # make the vertical names scrollbar move if path is moved
    def yScrollPath(self, *A):
        move = A[1]
        if self.filesNameList.yview() != self.filesPathList.yview():
            self.filesNameList.yview_moveto(move)
        self.filesScroll.set(*A)

    # make the horizontal names scrollbar move
    def xScrollName(self, *A):
        move = A[1]
        if A[0] == "scroll":
            self.filesNameList.xview_scroll(move, UNITS)
        elif A[0] == "moveto":
            self.filesNameList.xview_moveto(move)

    # make the horizontal path scrollbar move
    def xScrollPath(self, *A):
        move = A[1]
        if A[0] == "scroll":
            self.filesPathList.xview_scroll(move, UNITS)
        elif A[0] == "moveto":
            self.filesPathList.xview_moveto(move)

    # add the file found and its path to the lists
    def fileData(self, name, path):
        self.filesNameList.insert(END, name)
        self.filesPathList.insert(END, path)

    # select the same item from the path list when clicked the name list and copy the name to clipboard
    def selectNameList(self, event):
        selection = self.filesNameList.curselection()
        if selection:
            index = selection[0]
            name = self.filesNameList.get(index)
            self.clipboard_clear()
            self.clipboard_append(name)
            self.update()
            self.filesPathList.select_set(index)

    # select the same item from the name list when clicked the path list and copy the path to clipboard
    def selectPathList(self, event):
        selection = self.filesPathList.curselection()
        if selection:
            index = selection[0]
            path = self.filesPathList.get(index)
            self.clipboard_clear()
            self.clipboard_append(path)
            self.update()
            self.filesNameList.select_set(index)


top = Tk()
window(top)
app = Application(top)
app.mainloop()
