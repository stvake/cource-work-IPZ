class UnitProjectsController:
    def __init__(self, units_controller, unit_name, model, view):
        self.units_controller = units_controller
        self.model = model
        self.view = view
        self.tab = self.view.unit_projects_tabs[unit_name]
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.save_Button.config(command=self.save_tab)
        self.get_projects_from_db()

    def get_projects_from_db(self):
        info = self.model.get_unit_projects(self.tab.unit_name)
        try:
            for i in info:
                self.tab.projects_table.insert('', 'end', values=i)
        except TypeError:
            pass

    def save_tab(self):
        ...

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        try:
            self.units_controller.unit_projects.pop(self.tab.unit_name)
        except KeyError:
            pass
