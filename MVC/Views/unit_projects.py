from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame
from CustomWidgets.combobox_table import ComboboxTable


class UnitProjectsView:
    def __init__(self, notebook, unit_name):
        self.unit_name = unit_name
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

        self.projects_table = ComboboxTable(self.frame, columns=('ID', 'name', 'cost', 'start', 'end', 'collaborators'),
                                            show='headings', height=35,
                                            non_editable_columns=[0, 2, 3, 4, 5])
        self.projects_table.heading('ID', text='№')
        self.projects_table.heading('name', text='Назва проекту')
        self.projects_table.heading('cost', text='Вартість проекту')
        self.projects_table.heading('start', text='Дата початку проекту')
        self.projects_table.heading('end', text='Дата закінчення проекту')
        self.projects_table.heading('collaborators', text='Учасники проекту')

        self.projects_table.column('ID', width=30)
        self.projects_table.column('name', width=150)
        self.projects_table.column('cost', width=150)
        self.projects_table.column('start', width=150)
        self.projects_table.column('end', width=150)
        self.projects_table.column('collaborators', width=395)

        self.projects_table.pack(padx=5, pady=5, fill=BOTH)

        self.save_Button = ttk.Button(self.frame, text="Зберегти зміни")
        self.save_Button.pack(fill=BOTH, padx=5, pady=5)

        self.closeTab_Button = ttk.Button(self.frame, text="Закрити вкладку")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

        self.notebook.insert("end", self.mainFrame, text=f"Проекти підрозділу: {self.unit_name}")
        self.notebook.select(self.mainFrame)
