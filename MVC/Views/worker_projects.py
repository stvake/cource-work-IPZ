from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame
from CustomWidgets.editable_table import EditableTable


class WorkerProjectView:
    def __init__(self, notebook, worker):
        self.worker = worker

        self.id = worker.id

        self.name = worker.name_text.get(1.0, END)[:-1]

        self.notebook = notebook
        self.mainFrame = ttk.Frame(notebook)

        self.mainScrolledFrame = VerticalScrolledFrame(self.mainFrame)
        self.mainScrolledFrame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.projects_table = EditableTable(self.mainScrolledFrame, columns=('ID', 'name', 'cost', 'start', 'end',
                                                                             'collaborators'),
                                            show='headings', height=10, non_editable_columns=[0, 1, 2, 3, 4, 5],
                                            allow_delete=False)
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

        self.closeTab_Button = ttk.Button(self.mainScrolledFrame, text="Закрити вкладку")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

        self.notebook.insert("end", self.mainFrame, text="Проекти: " + self.name)
        self.notebook.select(self.mainFrame)
