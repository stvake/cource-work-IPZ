from MVC.Controllers.unit_projects import UnitProjectsController


class UnitsController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['Units'] = self.view.create_tab('Units')
        self.tab = self.view.tabs['Units']
        self.unit_projects = {}
        self.tab.sortByCost_Button.config(command=self.sort_by_cost)
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.tab.openUnitWorkers_Button.config(command=self.open_unit_workers)
        self.tab.openUnitProjects_Button.config(command=self.open_unit_projects)
        self.get_info_from_db()

    def get_info_from_db(self):
        rows = self.model.get_units()
        for row in rows:
            self.tab.units_table.insert('', 'end', values=tuple(row)[1:-1])

    def sort_by_cost(self):
        ...

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None

    def close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None

    def open_unit_workers(self):
        selected_iid = self.tab.units_table.focus()
        unit_name = self.tab.units_table.item(selected_iid).get('values')[0]
        print(self.model.get_unit_workers(unit_name))

    def open_unit_projects(self):
        selected_iid = self.tab.units_table.focus()
        unit_name = self.tab.units_table.item(selected_iid).get('values')[0]
        self.view.create_tab('UnitProjects', unit_name, self.tab.notebook, unit_name)
        self.unit_projects[unit_name] = UnitProjectsController(self, unit_name, self.model, self.view)
