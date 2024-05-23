class WorkerProjectsController:
    def __init__(self, worker_controller, model, view, worker_id):
        self.worker_controller = worker_controller
        self.model = model
        self.view = view
        self.worker_id = worker_id
        self.worker_projects_info = self.view.worker_projects_tabs[worker_id]
        self.worker_projects_info.closeTab_Button.config(command=self.close_tab)
        self.ready_to_save = 1
        self.get_projects_from_db(worker_id)

    def get_projects_from_db(self, worker_id):
        info = self.model.get_worker_projects(worker_id)
        for i in info:
            self.worker_projects_info.projects_table.insert('', 'end', values=i)

    def close_tab(self):
        self.worker_controller.worker_projects.pop(self.worker_id)
        self.worker_projects_info.notebook.forget(self.worker_projects_info.mainFrame)
