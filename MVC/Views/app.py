from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Відділ кадрів')
        self.geometry("1052x850")
        self.notebook = ttk.Notebook(self, width=1052, height=850)
