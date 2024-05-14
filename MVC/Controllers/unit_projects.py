class UnitProjectsController:
    def __init__(self, units_controller, unit_name, model, view):
        self.units_controller = units_controller
        self.unit_name = unit_name
        self.model = model
        self.view = view
        self.tab = self.view.unit_projects_tabs[unit_name]
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.save_Button.config(command=self.save_tab)
        self.tab.projects_table.on_value_selected = self.load_project_data
        self.initialize_combobox()
        self.get_projects_from_db()

    def initialize_combobox(self):
        self.tab.projects_table.set_combobox_values('name', self.model.get_projects_for_unit())

    def get_projects_from_db(self):
        info = self.model.get_unit_projects(self.unit_name)
        try:
            for i in info:
                self.tab.projects_table.insert('', 'end', values=i)
        except TypeError:
            pass

    def save_tab(self):
        self.model.set_unit_projects(','.join([str(i[0]) for i in self.tab.projects_table.get_all_rows()]),
                                     self.unit_name)
        self.units_controller.refresh()

    def load_project_data(self, value):
        data = self.model.get_project_data_by_name(value)
        self.tab.projects_table.item(self.tab.projects_table.focus(), values=data)

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        try:
            self.units_controller.unit_projects.pop(self.unit_name)
        except KeyError:
            pass
