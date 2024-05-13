from tkinter import *
from tkinter import ttk


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Відділ кадрів')
        self.width = 1070
        self.height = 860
        self.geometry(f"{self.width}x{self.height}")
        self.notebook = ttk.Notebook(self, width=self.width, height=self.height)
