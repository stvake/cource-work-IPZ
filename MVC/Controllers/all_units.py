class UnitsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Units']
        self.tab.sortByCost_Button.config(command=self.sortByCost)
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.tab.openUnitWorkers_Button.config(command=self.open_unit_workers)
        self.tab.openUnitProjects_Button.config(command=self.open_unit_projects)

    def sortByCost(self):
        pass

    def close_tab(self):
        pass

    def close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)

    def open_unit_workers(self):
        pass

    def open_unit_projects(self):
        pass
