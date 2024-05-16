import tkinter.ttk as ttk
from CustomWidgets.editable_table import EditableTable


class BestPostsView:
    def __init__(self, notebook):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(self.notebook)

        self.best_posts_table = EditableTable(self.mainFrame, columns=('№', 'Name', 'HourEarn'), show='headings')

        self.best_posts_table.heading('№', text="Рейтинг")
        self.best_posts_table.heading('Name', text="Назва посади")
        self.best_posts_table.heading('HourEarn', text="Заробіток за час")
        self.best_posts_table.pack()

        self.notebook.insert("end", self.mainFrame, text="5 найпривабливіших посад")
        self.notebook.select(self.mainFrame)

        self.close_button = ttk.Button(self.mainFrame, text="Закрити вкладку")
        self.close_button.pack()
