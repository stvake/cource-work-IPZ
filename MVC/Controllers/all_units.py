class UnitsController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['Units'] = self.view.create_tab('Units')
        self.tab = self.view.tabs['Units']
        self.tab.sortByCost_Button.config(command=self.sort_by_cost)
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.tab.openUnitWorkers_Button.config(command=self.open_unit_workers)
        self.tab.openUnitProjects_Button.config(command=self.open_unit_projects)

    def sort_by_cost(self):
        pass

    def close_tab(self):
        pass

    def close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None

    def open_unit_workers(self):
        pass

    def open_unit_projects(self):
        pass
