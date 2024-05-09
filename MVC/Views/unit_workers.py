from MVC.Views.all_workers import AllWorkersView


class UnitWorkers(AllWorkersView):
    def __init__(self, notebook, unit_name):
        self.unit_name = unit_name
        super().__init__(notebook)

    def add_tab(self):
        self.notebook.insert("end", self.mainFrame, text=f"Робітники підрозділу: {self.unit_name}")
        self.notebook.select(self.mainFrame)
