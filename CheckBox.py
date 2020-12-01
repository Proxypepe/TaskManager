from tkinter import *

class CheckBox(Checkbutton):
    def __init__(self, master: object = None, **options: str) -> object:
        Checkbutton.__init__(self, master)
        self.var = IntVar()
        self.chk = Checkbutton(master, variable=self.var, **options)
        self.chk.pack()

    def get_state(self):
        return self.var.get()
