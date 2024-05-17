from MVC.Controllers.worker import WorkerController


class BestWorkerController:
    def __init__(self, model, view, post_name):
        self.model = model
        self.view = view
        self.post_name = post_name
        self.tab = self.view.create_tab('BestWorker', self.post_name)
        self.tab.close_button.config(command=self.close_tab)
        self.worker_controller = None
        self.worker_id = None
        self.correlation = {}
        self.correlation1 = {}
        self.best_worker = []
        self.find_best_worker()
        self.show_best_worker()

    def find_best_worker(self):
        workers_hours = self.model.get_work_hours(self.post_name)
        project_cost = self.model.get_projects_cost()
        workers = self.model.get_all_worker()
        for i in workers:
            self.correlation[i[0]] = project_cost[i[1]]
        for i in workers_hours:
            try:
                if self.correlation[i[0]] / i[1] != 0:
                    self.correlation1[i[0]] = self.correlation[i[0]] / i[1]
            except ZeroDivisionError:
                pass
        for i in self.correlation1.items():
            self.best_worker.append(i)
        self.best_worker = sorted(self.best_worker, key=lambda x: x[1], reverse=True)
        self.worker_id = self.best_worker[-1][0]

    def show_best_worker(self):
        self.view.create_tab(
            'Worker',
            self.worker_id,
            self.worker_id,
            self.tab.worker_frame,
            self.tab.notebook
        )
        self.worker_controller = WorkerController(self, self.model, self.view, self.worker_id)

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
