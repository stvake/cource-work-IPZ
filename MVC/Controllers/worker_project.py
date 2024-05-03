from tkinter import *
from tkinter.messagebox import *


class WorkerProjectsController:
    def __init__(self, model, view, worker_id):
        self.model = model
        self.view = view
        self.worker_projects_info = self.view.worker_projects_tabs[worker_id]
        self.worker_projects_info.closeTab_Button.config(command=self.close_tab)
        self.worker_projects_info.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.ready_to_save = 1
        self.get_projects_from_db(worker_id)

    def get_projects_from_db(self, worker_id):
        pass

    def close_tab(self):
        pass

    def close_tab_without_save(self):
        self.worker_projects_info.notebook.forget(self.worker_projects_info.mainFrame)
