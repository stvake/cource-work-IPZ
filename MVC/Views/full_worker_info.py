from tkinter import *
import tkinter.ttk as ttk
from MVC.Views.add_new_worker import AddNewWorkerView


class FullWorkerInfoView(AddNewWorkerView):
    def __init__(self, notebook, worker):
        self.worker = worker
        self.id = worker.id
        self.name = worker.name_text.get(1.0, END)[:-1]
        super().__init__(notebook)

    def initialize_photo(self):
        self.photo_frame = ttk.Frame(self.mainFrame, relief=GROOVE)
        self.photo_frame.pack(side=LEFT, anchor=NW, padx=5, pady=10)
        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack(padx=2, pady=2)

    def initialize_buttons(self):
        self.closeTab_Button = ttk.Button(self.mainScrolledFrame.interior, text="Зберегти та закрити вкладку")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)
        self.closeTabWithoutSave_Button = ttk.Button(self.mainScrolledFrame.interior, text="Закрити без збереження")
        self.closeTabWithoutSave_Button.pack(fill=BOTH, padx=5, pady=5)

    def initialize_tab(self):
        self.notebook.insert("end", self.mainFrame, text=self.name)
