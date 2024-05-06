from MVC.Controllers.worker import WorkerController


class AllWorkersController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Workers']
        self.workers_controllers = {}
        self.tab.add_worker_button.config(command=self.add_worker)
        self.tab.close_button.config(command=self.close_tab)
        self.get_all_workers()

    def get_all_workers(self):
        for i in range(self.model.get_workers_quantity()):
            if self.model.if_exists('Workers', 'id', i+1):
                self.view.create_tab(
                    'Worker',
                    i+1,
                    i+1,
                    self.view.tabs['Workers'].frame.interior,
                    self.view.tabs['Workers'].notebook
                )
                self.workers_controllers[f'{i+1}'] = WorkerController(self, self.model, self.view, i+1)

    def add_worker(self):
        self.view.add_new_worker()

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)
