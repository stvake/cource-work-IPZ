from tkinter import TclError
from tkinter.messagebox import showwarning


class AllProjectsController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['AllProjects'] = self.view.create_tab('AllProjects')
        self.tab = self.view.tabs['AllProjects']
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.get_projects_from_db()

    def get_projects_from_db(self):
        info = self.model.get_all_projects()
        for i in info:
            self.tab.projects_table.insert('', 'end', values=i[1:])

    def close_tab(self):
        def get_all_rows(table):
            output = []
            n = 1
            try:
                while True:
                    output.append(table.item(f'I00{n}').get('values'))
                    n += 1
            except TclError:
                return output
        data = get_all_rows(self.tab.projects_table)
        if self.model.update_projects_table(data):
            showwarning("Зауваження", "Правильно заповніть поля.")
            return
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_projects = None

    def close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)
        self.main_controller.all_projects = None
