#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
from tkinter import Label, Button, Scale, Entry, Frame, HORIZONTAL

# from tkinter import ttk


class Application(tk.Tk):
    name = "ColorMishMash"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        self.bind("<Escape>", self.quit)

        self.lblMain = Label(self, text="ColoMishmash")
        self.lblMain.pack()
        self.btnQuit = Button(self, text="Quit", command=self.quit)
        self.btnQuit.pack()

        self.frameR = Frame(self)
        self.frameR.pack()
        self.frameG = Frame(self)
        self.frameG.pack()
        self.frameB = Frame(self)
        self.frameB.pack()

        self.varR = tk.IntVar()
        self.varG = tk.IntVar()
        self.varB = tk.IntVar()
        self.varR.trace("w", self.color_change)
        self.varG.trace("w", self.color_change)
        self.varB.trace("w", self.color_change)

        self.lblR = Label(self.frameR, text="R", fg="#ff0000")
        self.lblR.pack(side="left", anchor="s")
        self.scaleR = Scale(
            self.frameR,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varR,
        )
        self.scaleR.pack(side="left", anchor="s")
        self.entryR = Entry(self.frameR, width=5, textvariable=self.varR)
        self.entryR.pack(side="left", anchor="s")
        
        self.entryR.bind('<Key>', self.callback)

        self.lblG = Label(self.frameG, text="G", bg="#00ff00")
        self.lblG.pack(side="left", anchor="s")
        self.scaleG = Scale(
            self.frameG,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varG,
        )
        self.scaleG.pack(side="left", anchor="s")
        self.entryG = Entry(self.frameG, width=5, textvariable=self.varG)
        self.entryG.pack(side="left", anchor="s")

        self.lblB = Label(self.frameB, text="B")
        self.lblB.pack(side="left", anchor="s")
        self.scaleB = Scale(
            self.frameB,
            from_=0,
            to=0xFF,
            orient=HORIZONTAL,
            length=333,
            variable=self.varB,
        )
        self.scaleB.pack(side="left", anchor="s")
        self.entryB = Entry(self.frameB, width=5, textvariable=self.varB)
        self.entryB.pack(side="left", anchor="s")

        self.canvasMain = tk.Canvas(self, width=300, height=200, bg="#ffffff")
        self.canvasMain.pack()

        self.varMain = tk.StringVar(self, "#000000", "varMain")
        self.entryMain = tk.Entry(
            self,
            width=8,
            textvariable=self.varMain,
            state="readonly",
            readonlybackground="#FFFFFF",
        )
        self.entryMain.pack(anchor="e")

        self.frameMem = Frame(self)
        self.frameMem.pack()
        self.canvasMem = []
        for row in range(3):
            for column in range(7):
                canvas = tk.Canvas(self.frameMem, width=50, height=50, bg="#ef12ab")
                canvas.grid(row=row, column=column)
                self.canvasMem.append(canvas)
                canvas.bind('<Button-1>', self.clickHandler)
        self.canvasMain.bind('<Button-1>', self.clickHandler)

    def clickHandler(self, event):
        if self.cget('cursor') != 'pencil':    # kliknu poprve
            self.config(cursor='pencil')
            self.color = event.widget.cget('bg')
        else:                                  # kliknu podruhe
            self.config(cursor='')
            if event.widget is self.canvasMain:
                r = int(self.color[1:3], 16)
                g = int(self.color[3:5], 16)
                b = int(self.color[5:], 16)
                self.varR.set(r)
                self.varG.set(g)
                self.varB.set(b)
            else:
                event.widget.config(bg=self.color)

    def colorSave(self):
        with open('colors.txt', 'w') as f:
            f.write(self.canvasMain.cget('bg')+'\n')
            for canvas in self.canvasMem: 
                f.write(canvas.cget('bg')+'\n')

    def callback(self, event):
        print( event.keycode, event.keysym, event.keysym_num, event.x, event.y )

    def color_change(self, var=None, index=None, mode=None):
        r = self.varR.get()
        g = self.varG.get()
        b = self.varB.get()
        colorstring = f"#{r:02X}{g:02X}{b:02X}"
        self.canvasMain.config(bg=colorstring)

        # self.entryMain.delete(0, 'end')
        # self.entryMain.insert(0, colorstring)
        self.varMain.set(colorstring)

    def quit(self, event=None):
        self.colorSave()
        super().quit()


app = Application()
app.mainloop()
