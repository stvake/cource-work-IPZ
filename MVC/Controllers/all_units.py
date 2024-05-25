from MVC.Controllers.unit_projects import UnitProjectsController
from MVC.Controllers.unit_workers import UnitWorkersController

from tkinter import TclError


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
        self.units = self.model.get_units()
        for row in self.units:
            self.tab.units_table.insert('', 'end', values=tuple(row)[1][:-1])
        self.rows = self.tab.units_table.get_all_rows()
        self.rows_iid = self.tab.units_table.get_children()

    def refresh(self):
        self.tab.recreate_table()
        self._get_info_from_db()

    def _sort_by_cost(self, reset=False):
        self.sorted_items = []
        if reset:
            self.sorted_items = self.rows.copy()
        else:
            items = self.tab.units_table.get_all_rows()
            if self.sort_count == 0:
                self.sorted_items = sorted(items, key=lambda item: item[-1])
                self.sort_count = 1
            elif self.sort_count == 1:
                self.sorted_items = sorted(items, key=lambda item: item[-1], reverse=True)
                self.sort_count = 2
            else:
                self.sort_count = 0
                self._sort_by_cost(reset=True)

        for i in range(len(self.rows_iid)):
            try:
                self.tab.units_table.item(self.rows_iid[i], values=self.sorted_items[i])
            except TclError:
                pass

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
        old_units = [(i[0], i[1][0]) for i in self.units]
        units = [i[0] for i in self.tab.units_table.get_all_rows()]
        ids = self.tab.units_table.get_children()

        if int(ids[-1][1:], 16) != len(old_units):
            for i in range(abs(int(ids[-1][1:], 16)-len(old_units))):
                old_units.append(([], None))

        new_units = [(old_units[int(ids[i][1:])-1][0], units[i]) for i in range(len(units))]

        self.model.update_units(old_units, new_units, ids)
        self.refresh()

    def _close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_units_controller = None
