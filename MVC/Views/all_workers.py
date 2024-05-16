from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame


class AllWorkersView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.sort_button_frame = ttk.Frame(self.mainFrame)
        self.sort_button_frame.pack(fill=BOTH)

        self.add_worker_button = ttk.Button(self.sort_button_frame, text='Додати')
        self.add_worker_button.pack(anchor=W, padx=5, pady=5, side=LEFT)
        self.sort_firstname = ttk.Button(self.sort_button_frame, text="Відсортувати за ім'ям")
        self.sort_firstname.pack(anchor=E, padx=5, pady=5, side=RIGHT)
        self.sort_lastname = ttk.Button(self.sort_button_frame, text="Відсортувати за прізвищем")
        self.sort_lastname.pack(anchor=E, padx=5, pady=5, side=RIGHT)
        self.sort_salary = ttk.Button(self.sort_button_frame, text="Відсортувати за заробітною платою")
        self.sort_salary.pack(anchor=E, padx=5, pady=5, side=RIGHT)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

        self.close_button = ttk.Button(self.mainFrame, text="Закрити вкладку")
        self.close_button.pack(padx=5, pady=5, side=BOTTOM, fill=BOTH)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Список робітників")
        self.notebook.select(self.mainFrame)
