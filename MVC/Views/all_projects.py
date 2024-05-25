from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame
from CustomWidgets.editable_table import EditableTable


class AllProjectsView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

        self.projects_table = EditableTable(self.frame, columns=('ID', 'name', 'cost', 'start', 'end', 'collaborators'),
                                            show='headings', height=35, allow_delete=False)
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

        self.closeTab_Button = ttk.Button(self.frame, text="Зберегти та закрити вкладку")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

        self.closeTabWithoutSave_Button = ttk.Button(self.frame, text="Закрити вкладку без збереження")
        self.closeTabWithoutSave_Button.pack(fill=BOTH, padx=5, pady=5)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Всі проекти")
        self.notebook.select(self.mainFrame)
