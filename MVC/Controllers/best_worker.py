from MVC.Controllers.worker import WorkerController


class BestWorkerController:
    def __init__(self, model, view, post_name):
        self.model = model
        self.view = view
        self.post_name = post_name
        self.tab = self.view.create_tab('BestWorker', self.post_name)
        self.tab.close_button.config(command=self.close_tab)
        self.worker_id = None
        self.worker_controller = None
        self.find_best_worker()
        self.show_best_worker()

    def find_best_worker(self):
        ...

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
