import tkinter.ttk as ttk


class HomeView:
    def __init__(self, notebook):
        self.notebook = notebook
        self.main_tab = ttk.Frame(self.notebook)

        self.workers_Button = ttk.Button(self.main_tab, text="Список всіх робітників", width=25)
        self.listOfAllUnits_Button = ttk.Button(self.main_tab, text="Список підрозділів", width=25)
        self.position_Button = ttk.Button(self.main_tab, text="Список посад", width=25)
        self.search_Button = ttk.Button(self.main_tab, text="Пошук", width=25)

        self.workers_Button.pack()
        self.listOfAllUnits_Button.pack()
        self.position_Button.pack()
        self.search_Button.pack()

        self.notebook.add(self.main_tab, text="Головна сторінка")
        self.notebook.pack(padx=5, pady=5, expand=True)
