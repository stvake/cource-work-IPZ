from tkinter import *
import tkinter.ttk as ttk
from MVC.Views.vertical_scrolled_frame import VerticalScrolledFrame


class AllUnitsView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Список підрозділів")
        self.notebook.select(self.mainFrame)
