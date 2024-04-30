class HomeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Home']
        self._bind()

    def _bind(self):
        self.tab.workers_Button.config(command=self.open_workers)
        self.tab.listOfAllUnits_Button.config(command=self.open_units)
        self.tab.position_Button.config(command=self.open_positions)
        self.tab.search_Button.config(command=self.open_search)

    def open_workers(self):
        self.view.tabs['Workers'].add_tab()

    def open_units(self):
        self.view.tabs['Units'].add_tab()

    def open_positions(self):
        self.view.tabs['Positions'].add_tab()

    def open_search(self):
        self.view.tabs['Search'].add_tab()
