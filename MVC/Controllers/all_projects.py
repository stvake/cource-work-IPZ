from tkinter import TclError


class AllProjectsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.tabs['AllProjects']
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.get_projects_from_db()

    def get_projects_from_db(self):
        info = self.model.get_all_projects()
        for i in info:
            values = (list(i[1:-1]) +
                      [", ".join([" ".join(self.model.get_worker_name(j)) for j in [i[0]]+i[-1].split(',')])])
            self.tab.projects_table.insert('', 'end', values=tuple(values))

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
        self.model.update_projects_table(data)
        self.tab.notebook.forget(self.tab.mainFrame)

    def close_tab_without_save(self):
        self.tab.notebook.forget(self.tab.mainFrame)
