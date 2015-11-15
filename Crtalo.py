from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from random import randint

class Crtalo(Frame):
    def __init__(self, root = Tk()):
        self.R = root
        super().__init__(root)
        self.createGUI()
        self.pack(fill = BOTH, expand = True)
        return

    def createGUI(self):
        self.X0 = None
        self.Y0 = None
        self.COLOR = None
        self.L = None
        self.U = []
        self.Re = []
        self.K = "L"
        
        self.C = Canvas(self, bg = "#FFFFFF")
        self.C.pack(fill = BOTH, expand = True)

        self.R.bind("<Control-E>", self.toOval)
        self.R.bind("<Control-e>", self.toOval)
        self.R.bind("<Control-L>", self.toLine)
        self.R.bind("<Control-l>", self.toLine)
        self.R.bind("<Control-R>", self.toRect)
        self.R.bind("<Control-r>", self.toRect)
        self.R.bind("<Control-Z>", self.undo)
        self.R.bind("<Control-z>", self.undo)
        self.R.bind("<Control-Y>", self.redo)
        self.R.bind("<Control-y>", self.redo)
        self.R.bind("<Control-S>", self.save)
        self.R.bind("<Control-s>", self.save)
        self.R.bind("<Control-O>", self.open)
        self.R.bind("<Control-o>", self.open)
        
        self.C.bind("<Button-1>", self.press)
        self.C.bind("<B1-Motion>", self.rect)
        self.C.bind("<ButtonRelease-1>", self.rel)
        return
    
    def press(self, e):
        self.X0 = e.x
        self.Y0 = e.y

        r = hex(randint(0, 255))[2:]
        r = "0" * (2 - len(r)) + r
        g = hex(randint(0, 255))[2:]
        g = "0" * (2 - len(g)) + g
        b = hex(randint(0, 255))[2:]
        b = "0" * (2 - len(b)) + b
        self.COLOR = "#" + r + g+ b

        if self.K == "R":
            self.L = self.C.create_rectangle(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "O":
            self.L = self.C.create_oval(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "L":
            self.L = self.C.create_line(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        return

    def rect(self, e):
        self.C.delete(self.L)
        
        if self.K == "R":
            self.L = self.C.create_rectangle(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "O":
            self.L = self.C.create_oval(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "L":
            self.L = self.C.create_line(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        return

    def rel(self, e):
        self.C.delete(self.L)
        
        if self.K == "R":
            self.L = self.C.create_rectangle(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "O":
            self.L = self.C.create_oval(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)
        elif self.K == "L":
            self.L = self.C.create_line(self.X0, self.Y0, e.x, e.y, fill = self.COLOR)

        self.U.append((self.L, self.K, self.X0, self.Y0, e.x, e.y, self.COLOR))
            
        self.COLOR = None
        self.X0 = None
        self.Y0 = None
        self.L = None
        return

    def toRect(self, e):
        self.K = "R"
        return

    def toOval(self, e):
        self.K = "O"
        return

    def toLine(self, e):
        self.K = "L"
        return

    def undo(self, e):
        self.Re.append(self.U[-1])
        self.C.delete(self.U[-1][0])
        del(self.U[-1])
        return

    def redo(self, e):
        l = self.Re[-1]
        self.U.append(l)
        if l[1] == "R":
            self.C.create_rectangle(l[2], l[3], l[4], l[5], fill = l[6])
        elif l[1] == "O":
            self.C.create_oval(l[2], l[3], l[4], l[5], fill = l[6])
        elif l[1] == "L":
           self.C.create_line(l[2], l[3], l[4], l[5], fill = l[6])

        del(self.Re[-1])
        return

    def save(self, e):
        try:
            fn = asksaveasfilename(defaultextension = ".pcd", filetypes = [('PCD file','*.pcd')])
            f = open(fn, "w")
            txt = "#PCD FILE - DO NOT EDIT THE CONTENTS!\n"
            for i in range(len(self.U)):
                ID, t, x0, y0, x1, y1, c = self.U[i]
                txt += t + " " + str(x0) + " " + str(y0) + " " + str(x1) + " " + str(y1) + " " + c + "\n"
            f.write(txt)
            f.close()
        except:
            return
        return

    def open(self, e):
        try:
            fn = askopenfilename(defaultextension = ".pcd", filetypes = [('PCD file','*.pcd')])
            f = open(fn, "r")
            self.C.delete(ALL)
            r = f.readline()
            while r != "":
                if r[0] != "#":
                    t, x0, y0, x1, y1, c = r.split(" ")
                    if t == "L":
                        self.C.create_line(int(x0), int(y0), int(x1), int(y1), fill = c)
                    elif t == "R":
                        self.C.create_rectangle(int(x0), int(y0), int(x1), int(y1), fill = c)
                    elif t == "O":
                        self.C.create_oval(int(x0), int(y0), int(x1), int(y1), fill = c)
                r = f.readline()
            self.U = []
            self.R = []
        except:
            return
        return
    
Crtalo()
mainloop()
