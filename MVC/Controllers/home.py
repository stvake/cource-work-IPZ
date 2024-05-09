class HomeController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Home']
        self._bind()

    def _bind(self):
        self.tab.workers_Button.config(command=self.open_workers)
        self.tab.listOfAllUnits_Button.config(command=self.open_units)
        self.tab.listOfAllProjects_Button.config(command=self.open_projects)
        self.tab.position_Button.config(command=self.open_positions)
        self.tab.search_Button.config(command=self.open_search)

    def open_workers(self):
        self.main_controller.create_all_workers_controller()
        self.view.tabs['Workers'].add_tab()

    def open_units(self):
        self.main_controller.create_all_units_controller()
        self.view.tabs['Units'].add_tab()

    def open_projects(self):
        self.main_controller.create_all_projects_controller()
        self.view.tabs['AllProjects'].add_tab()

    def open_positions(self):
        self.main_controller.create_all_positions_controller()
        self.view.tabs['Positions'].add_tab()

    def open_search(self):
        self.main_controller.create_search_controller()
        self.view.tabs['Search'].add_tab()
