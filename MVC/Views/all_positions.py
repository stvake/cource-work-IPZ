from tkinter import *
import tkinter.ttk as ttk
from CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame
from CustomWidgets.editable_table import EditableTable


class AllPositionsView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.frame = VerticalScrolledFrame(self.mainFrame)
        self.frame.pack(expand=True, fill=BOTH)

        self.post_table = EditableTable(self.frame, columns=('Name', 'salary', 'time', 'amount', 'summ_salary'),
                                              show='headings', height=10)
        self.post_table.heading('Name', text='Назва посади')
        self.post_table.heading('salary', text='Заробітня плата')
        self.post_table.heading('time', text='Кількість робочих годин')
        self.post_table.heading('amount', text='Кількість працівників')
        self.post_table.heading('summ_salary', text='Сума заробітньої плати')
        self.post_table.pack()

        self.bestWorker_Button = ttk.Button(self.frame, text="Відкрити справу найкращього працівника на вибраній посаді")
        self.bestWorker_Button.pack(fill=BOTH, padx=5, pady=5)

        self.bestPosts_Button = ttk.Button(self.frame, text="Відкрити вкладку з найбільш привабливими посадами")
        self.bestPosts_Button.pack(fill=BOTH, padx=5, pady=5)

        self.save_Button = ttk.Button(self.frame, text="Зберегти")
        self.save_Button.pack(fill=BOTH, padx=5, pady=5)

        self.closeTab_Button = ttk.Button(self.frame, text="Закрити")
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text="Список посад")
        self.notebook.select(self.mainFrame)
