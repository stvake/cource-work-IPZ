from tkinter import *
import tkinter.ttk as ttk


class BestWorkerView:
    def __init__(self, notebook, post_name):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.notebook.insert("end", self.mainFrame, text="Найкращий працівник на посаді:" + post_name)
        self.notebook.select(self.mainFrame)

        self.close_button = ttk.Button(self.mainFrame, text="Закрити вкладку")
        self.close_button.pack()