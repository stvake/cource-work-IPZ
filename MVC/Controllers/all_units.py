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
        self.tab.saveTab_Button.config(command=self._save)
        self.tab.closeTab_Button.config(command=self._close_tab)
        self.tab.openUnitWorkers_Button.config(command=self._open_unit_workers)
        self.tab.openUnitProjects_Button.config(command=self._open_unit_projects)
        self.sort_count = 0
        self._get_info_from_db()

    def _get_info_from_db(self):
        rows = self.model.get_units()
        for row in rows:
            self.tab.units_table.insert('', 'end', values=tuple(row)[:-1])

    def refresh(self):
        self.tab.units_table.delete(*self.tab.units_table.get_children())
        self._get_info_from_db()

    def _sort_by_cost(self):
        items = [self.tab.units_table.item(line).get('values') for line in self.tab.units_table.get_children()]
        if self.sort_count == 0:
            sorted_items = sorted(items, key=lambda item: item[-1])
            self.sort_count = 1
        else:
            sorted_items = sorted(items, key=lambda item: item[-1], reverse=True)
            self.sort_count = 0

        rows_iid = self.tab.units_table.get_children()
        for i in range(len(rows_iid)):
            self.tab.units_table.item(rows_iid[i], values=sorted_items[i])

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

    def _save(self):
        units = [i[0] for i in self.tab.units_table.get_all_rows()]
        self.model.update_units(units)

    def _close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None
