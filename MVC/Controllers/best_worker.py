class BestWorkerController:
    def __init__(self, model, view, post_name):
        self.model = model
        self.view = view
        self.post_name = post_name
        self.tab = self.view.create_tab('BestWorker', self.post_name)
        self.tab.close_button.config(command=self.close_tab)
        self.find_best_worker()

    def find_best_worker(self):
        pass

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)