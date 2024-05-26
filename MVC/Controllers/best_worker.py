from MVC.Controllers.worker import WorkerController

from tkinter.messagebox import showwarning


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
        if not self.find_best_worker():
            self.show_best_worker()
        else:
            self.close_tab()
            showwarning("Увага", "На даній посаді немає працівників.")

    def find_best_worker(self):
        workers_hours = self.model.get_work_hours(self.post_name)
        project_cost = self.model.get_projects_cost()
        workers = self.model.get_all_worker()
        for i in workers:
            self.correlation[i[0]] = project_cost[i[1]]
        for i in workers_hours:
            try:
                self.correlation1[i[0]] = self.correlation[i[0]] / i[1]
            except ZeroDivisionError:
                showwarning("Увага", "На даній посаді у працівника нульовий стаж.")
                return
        for i in self.correlation1.items():
            self.best_worker.append(i)
        self.best_worker = sorted(self.best_worker, key=lambda x: x[1], reverse=True)
        try:
            self.worker_id = self.best_worker[0][0]
        except IndexError:
            return 'err'

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
