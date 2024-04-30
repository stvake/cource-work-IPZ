from tkinter import *
import tkinter.ttk as ttk
from MVC.Views.vertical_scrolled_frame import VerticalScrolledFrame


class AllWorkersView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.add_worker_button = ttk.Button(self.mainFrame, text='Додати')
        self.add_worker_button.pack(anchor=W, padx=5, pady=5)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Список робітників")
