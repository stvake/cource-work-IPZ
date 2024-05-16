import tkinter.ttk as ttk
from tkinter import LabelFrame

from PIL import ImageTk, Image


class HomeView:
    def __init__(self, notebook):
        self.notebook = notebook
        self.main_tab = ttk.Frame(self.notebook)

        self.background_image = ImageTk.PhotoImage(Image.open('photos/background.png'))
        self.background = ttk.Label(self.main_tab, image=self.background_image)
        self.background.pack(fill='both', expand=True)

        self.buttons_frame = LabelFrame(self.background, text='Кнопки управління', font=('Calibri', 12))
        self.buttons_frame.pack(side='left', anchor='sw')

        self.workers_Button = ttk.Button(self.buttons_frame, text="\nСписок всіх робітників\n", width=45)
        self.listOfAllUnits_Button = ttk.Button(self.buttons_frame, text="\nСписок підрозділів\n", width=45)
        self.listOfAllProjects_Button = ttk.Button(self.buttons_frame, text="\nСписок проектів\n", width=45)
        self.position_Button = ttk.Button(self.buttons_frame, text="\nСписок посад\n", width=45)

        self.workers_Button.pack(padx=2, pady=2)
        self.listOfAllUnits_Button.pack(padx=2, pady=2)
        self.listOfAllProjects_Button.pack(padx=2, pady=2)
        self.position_Button.pack(padx=2, pady=2)

        self.notebook.add(self.main_tab, text="Головна сторінка")
        self.notebook.pack(padx=5, pady=5, expand=True)

