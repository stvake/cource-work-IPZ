from MVC.Controllers.best_posts import BestPostsController
from MVC.Controllers.best_worker import BestWorkerController

from tkinter.messagebox import showwarning


class PositionsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.tabs['Positions'] = self.view.create_tab('Positions')
        self.tab = self.view.tabs['Positions']
        self.tab.save_Button.config(command=self.save)
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.bestWorker_Button.config(command=self.open_best_worker_info)
        self.tab.bestPosts_Button.config(command=self.open_best_posts)
        self.worker = None
        self.worker_id = None
        self.best_post_controller = None
        self.best_worker_controller = None
        self.post_name = None
        self.full_worker_info = {}

        self.post_id = int()
        self.get_posts_from_db()

    def get_posts_from_db(self):
        rows = self.model.get_posts()
        for row in rows:
            self.tab.post_table.insert('', 'end', values=tuple(row))

    def save(self):
        all_elements = self.tab.post_table.get_all_rows()
        if self.model.write_post([i[:-2] for i in all_elements]):
            showwarning("Увага", "Змініть дані.")

    def close_tab(self):
        self.tab.notebook.forget(self.tab.mainFrame)

    def open_best_worker_info(self):
        selected_iid = self.tab.post_table.focus()
        if selected_iid:
            self.post_name = self.tab.post_table.item(selected_iid).get('values')[0]
            self.best_worker_controller = BestWorkerController(self.model, self.view, self.post_name)

    def open_best_posts(self):
        self.best_post_controller = BestPostsController(self.model, self.view)
