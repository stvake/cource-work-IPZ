from MVC.Controllers.unit_projects import UnitProjectsController
from MVC.Controllers.unit_workers import UnitWorkersController


class UnitsController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['Units'] = self.view.create_tab('Units')
        self.tab = self.view.tabs['Units']
        self.unit_projects = {}
        self.unit_workers = {}
        self.tab.sortByCost_Button.config(command=self._sort_by_cost)
        self.tab.closeTab_Button.config(command=self._close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self._close_tab_without_save)
        self.tab.openUnitWorkers_Button.config(command=self._open_unit_workers)
        self.tab.openUnitProjects_Button.config(command=self._open_unit_projects)
        self._get_info_from_db()

    def _get_info_from_db(self):
        rows = self.model.get_units()
        for row in rows:
            self.tab.units_table.insert('', 'end', values=tuple(row)[:-1])

    def _sort_by_cost(self):
        ...

    def _open_unit_workers(self):
        selected_iid = self.tab.units_table.focus()
        if selected_iid:
            unit_name = self.tab.units_table.item(selected_iid).get('values')[0]
            self.unit_workers[unit_name] = UnitWorkersController(self.main_controller, self.model, self.view, unit_name)

    def _open_unit_projects(self):
        selected_iid = self.tab.units_table.focus()
        if selected_iid:
            unit_name = self.tab.units_table.item(selected_iid).get('values')[0]
            self.view.create_tab('UnitProjects', unit_name, self.tab.notebook, unit_name)
            self.unit_projects[unit_name] = UnitProjectsController(self, unit_name, self.model, self.view)

    def _close_tab(self):
        units = [self.tab.units_table.item(line).get('values')[0] for line in self.tab.units_table.get_children()]
        projects = [self.tab.units_table.item(line).get('values')[-1] for line in self.tab.units_table.get_children()]
        self.model.update_units(units, projects)
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None

    def _close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None
