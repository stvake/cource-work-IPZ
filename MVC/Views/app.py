from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Відділ кадрів')
        self.notebook = ttk.Notebook(self)
