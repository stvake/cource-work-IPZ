from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame
from CustomWidgets.editable_table import EditableTable


class AllUnitsView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

        self.sortByCost_Button = ttk.Button(self.frame, text="Відсортувати за сумарною вартістю проектів")
        self.sortByCost_Button.pack(anchor=E, padx=5, pady=5)

        self.table_frame = ttk.Frame(self.frame)
        self.table_frame.pack(fill=X, side=TOP)

        self._initialize_table()

        self.openUnitWorkers_Button = ttk.Button(self.frame,
                                                 text="Відкрити список всіх робітників вибраного підрозділу")
        self.openUnitWorkers_Button.pack(fill=BOTH, padx=5, pady=5)

        self.openUnitProjects_Button = ttk.Button(self.frame,
                                                  text="Відкрити вкладку всіх проектів вибраного підрозділу")
        self.openUnitProjects_Button.pack(fill=BOTH, padx=5, pady=5)

        self.saveTab_Button = ttk.Button(self.frame, text="Зберегти зміни")
        self.saveTab_Button.pack(fill=BOTH, padx=5, pady=5)

        self.closeTab_Button = ttk.Button(self.frame, text="Закрити вкладку")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

    def _initialize_table(self):
        self.units_table = EditableTable(self.table_frame,
                                         columns=('Name', 'number_of_workers', 'number_of_active_projects',
                                                  'number_of_all_projects', 'projects_cost'),
                                         show='headings', height=30, non_editable_columns=[1, 2, 3, 4])
        self.units_table.heading('Name', text='Назва підрозділу')
        self.units_table.heading('number_of_workers', text='Кількість робітників')
        self.units_table.heading('number_of_active_projects', text='Кількість незавершених проектів')
        self.units_table.heading('number_of_all_projects', text='Кількість всіх проектів')
        self.units_table.heading('projects_cost', text='Сумарна вартість усіх проектів')
        self.units_table.pack(padx=5, pady=5)

    def recreate_table(self):
        self.units_table.destroy()
        self._initialize_table()

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Список підрозділів")
        self.notebook.select(self.mainFrame)
