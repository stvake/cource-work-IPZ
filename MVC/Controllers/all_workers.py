import locale

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
        self.sort_salary_counter = 0
        self._initialize_tab()
        self._get_all_workers()
        self.sort_by('LastName')

    def _initialize_tab(self):
        self.view.tabs['Workers'] = self.view.create_tab('Workers')
        self.tab = self.view.tabs['Workers']
        self.tab.sort_lastname.config(command=lambda: self.sort_by('LastName'))
        self.tab.sort_firstname.config(command=lambda: self.sort_by('FirstName'))
        self.tab.sort_salary.config(command=lambda: self.sort_by('salary'))
        self.tab.add_worker_button.config(command=self.add_worker)
        self.tab.close_button.config(command=self.close_tab)

    def _get_all_workers(self, sort_by='LastName', reverse=False):
        if not self.workers_controllers:
            for i in self.model.get_id_of_workers():
                self.view.create_tab(
                    'Worker',
                    i,
                    i,
                    self.tab.frame.interior,
                    self.tab.notebook
                )
                self.workers_controllers[f'{i}'] = WorkerController(self, self.model, self.view, i)

        else:
            sorted_ids = []

            if sort_by == 'LastName':
                ids = [(i, self.workers_controllers[i].worker.name_text.get(1.0, 'end-1c').split()[0])
                       for i in self.workers_controllers]
                sorted_ids = [i[0] for i in sorted(ids, key=lambda x: locale.strxfrm(x[1]), reverse=reverse)]
            elif sort_by == 'FirstName':
                ids = [(i, self.workers_controllers[i].worker.name_text.get(1.0, 'end-1c').split()[1])
                       for i in self.workers_controllers]
                sorted_ids = [i[0] for i in sorted(ids, key=lambda x: locale.strxfrm(x[1]), reverse=reverse)]
            elif sort_by == 'salary':
                ids = [(i, int(self.workers_controllers[i].worker.salary_text.get(1.0, 'end-1c')))
                       for i in self.workers_controllers]
                sorted_ids = [i[0] for i in sorted(ids, key=lambda x: x[1], reverse=reverse)]

            for i in self.tab.frame.interior.winfo_children():
                i.destroy()

            for i in sorted_ids:
                self.view.create_tab(
                    'Worker',
                    i,
                    i,
                    self.tab.frame.interior,
                    self.tab.notebook
                )
                self.workers_controllers[f'{i}'] = WorkerController(self, self.model, self.view, i)

    def refresh(self):
        self._get_all_workers()

    def sort_by(self, sort_by):
        if sort_by == 'LastName':
            if self.sort_lastname_counter == 0:
                self._get_all_workers()
                self.sort_lastname_counter = 1
            else:
                self._get_all_workers(reverse=True)
                self.sort_lastname_counter = 0
        elif sort_by == 'FirstName':
            if self.sort_firstname_counter == 0:
                self._get_all_workers('FirstName')
                self.sort_firstname_counter = 1
            else:
                self._get_all_workers('FirstName', True)
                self.sort_firstname_counter = 0
        else:
            if self.sort_salary_counter == 0:
                self._get_all_workers('salary')
                self.sort_salary_counter = 1
            else:
                self._get_all_workers('salary', True)
                self.sort_salary_counter = 0

    def add_worker(self):
        self.main_controller.create_add_new_worker_controller()

    def close_tab(self):
        self.view.worker_tabs.clear()
        self.workers_controllers.clear()
        self.tab.notebook.forget(self.tab.mainFrame)
