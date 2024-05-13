from MVC.Controllers.worker import WorkerController


class AllWorkersController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.tab = None
        self.workers_controllers = {}
        self.sort_lastname_counter = 0
        self.sort_firstname_counter = 0
        self._initialize_tab()
        self._get_all_workers()

    def _initialize_tab(self):
        self.view.tabs['Workers'] = self.view.create_tab('Workers')
        self.tab = self.view.tabs['Workers']
        self.tab.sort_lastname.config(command=lambda: self.sort_by('LastName'))
        self.tab.sort_firstname.config(command=lambda: self.sort_by('FirstName'))
        self.tab.add_worker_button.config(command=self.add_worker)
        self.tab.close_button.config(command=self.close_tab)

    def _get_all_workers(self, sort_by='LastName', reverse=False):
        for i in self.model.get_id_of_workers_sorted_by(sort_by, reverse):
            self.view.create_tab(
                'Worker',
                i,
                i,
                self.view.tabs['Workers'].frame.interior,
                self.view.tabs['Workers'].notebook
            )
            self.workers_controllers[f'{i}'] = WorkerController(self, self.model, self.view, i)

    def sort_by(self, sort_by):
        self.view.worker_tabs.clear()
        self.workers_controllers.clear()
        for i in self.tab.frame.interior.winfo_children():
            i.destroy()

        if sort_by == 'LastName':
            if self.sort_lastname_counter == 0:
                self._get_all_workers()
                self.sort_lastname_counter = 1
            else:
                self._get_all_workers(reverse=True)
                self.sort_lastname_counter = 0
        else:
            if self.sort_firstname_counter == 0:
                self._get_all_workers('FirstName')
                self.sort_firstname_counter = 1
            else:
                self._get_all_workers('FirstName', True)
                self.sort_firstname_counter = 0

    def add_worker(self):
        self.main_controller.create_add_new_worker_controller()

    def close_tab(self):
        self.view.worker_tabs.clear()
        self.workers_controllers.clear()
        self.tab.notebook.forget(self.tab.mainFrame)
