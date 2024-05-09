from MVC.Controllers.worker import WorkerController


class UnitWorkersController:
    def __init__(self, main_controller, model, view, unit_name):
        self.unit_name = unit_name
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['UnitWorkers'] = self.view.create_tab('UnitWorkers', self.view.app.notebook, unit_name)
        self.tab = self.view.tabs['UnitWorkers']
        self.tab.add_tab()
        self.workers_controllers = {}
        self.tab.add_worker_button.config(command=self.add_worker)
        self.tab.close_button.config(command=self.close_tab)
        self.get_all_workers()

    def get_all_workers(self):
        for i in self.model.get_unit_workers(self.unit_name):
            self.view.create_tab(
                'Worker',
                i,
                i,
                self.tab.frame.interior,
                self.tab.notebook
            )
            self.workers_controllers[f'{i}'] = WorkerController(self, self.model, self.view, i)

    def add_worker(self):
        self.main_controller.create_add_new_worker_controller()

    def close_tab(self):
        self.view.worker_tabs.clear()
        self.workers_controllers.clear()
        self.tab.notebook.forget(self.tab.mainFrame)
