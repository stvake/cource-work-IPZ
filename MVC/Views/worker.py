from tkinter import *
import tkinter.ttk as ttk


class WorkerView(ttk.Frame):
    def __init__(self, worker_id, parent, notebook):
        super().__init__(parent)

        self.notebook = notebook

        self.id = worker_id
        self.info_page = None

        self.config(relief=GROOVE)
        self.pack(padx=5, pady=5, anchor=W)

        self.photo = None
        self.photo_frame = ttk.Frame(self, relief=GROOVE)
        self.photo_frame.pack(side=LEFT, anchor=W, padx=5, pady=5)

        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack(padx=2, pady=2)

        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.name_label = ttk.Label(self.info_frame, text="ПІБ:")
        self.name_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.email_label = ttk.Label(self.info_frame, text="Email:")
        self.email_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.birth_date_label = ttk.Label(self.info_frame, text="Дата народження:")
        self.birth_date_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.post_label = ttk.Label(self.info_frame, text="Посада:")
        self.post_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.name_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.name_text.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.email_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.email_text.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.birth_date_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.birth_date_text.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        self.post_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.post_text.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

        self.button_view = ttk.Button(self.buttons_frame, text="Докладніше")
        self.button_view.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.button_delete = ttk.Button(self.buttons_frame, text="Видалити")
        self.button_delete.grid(row=2, column=1, sticky=W, padx=5, pady=5)
