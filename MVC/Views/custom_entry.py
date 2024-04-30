from tkinter import *
import tkinter.ttk as ttk


class CustomEntry(ttk.Entry):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.associated_row = None
