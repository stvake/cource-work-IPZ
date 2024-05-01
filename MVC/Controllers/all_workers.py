class AllWorkersController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.tab = self.view.tabs['Workers']
        self.workers = {}
        self.tab.add_worker_button.config(command=self.add_worker)
        self.get_all_workers()

    def get_all_workers(self):
        for i in range(self.model.get_workers_quantity()):
            self.view.create_tab(
                i+1,
                'Worker',
                i+1,
                self.view.tabs['Workers'].frame.interior,
                self.view.tabs['Workers'].notebook
            )

    def add_worker(self):
        self.view.add_new_worker()
