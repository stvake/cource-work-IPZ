from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

from MVC.Controllers.full_worker_info import FullWorkerInfoController
from MVC.Controllers.worker_projects import WorkerProjectsController


class WorkerController:
    def __init__(self, all_workers_controller, model, view, worker_id):
        self.all_workers_controller = all_workers_controller
        self.model = model
        self.view = view
        self.worker = self.view.worker_tabs[worker_id]
        self.worker.button_view.config(command=self.more_info)
        self.worker.button_delete.config(command=self.delete_worker)
        self.worker.button_projects.config(command=self.open_projects)
        self.full_worker_info = {}
        self.worker_projects = {}
        self.get_info()

    def get_info(self):
        info = self.model.get_worker_info(self.worker.id)
        self.worker.name_text.config(state=NORMAL)
        self.worker.birth_date_text.config(state=NORMAL)
        self.worker.post_text.config(state=NORMAL)

        self.worker.name_text.insert(1.0, f"{info[1]} {info[2]} {info[3]}")
        self.worker.birth_date_text.insert(1.0, f"{info[4]}")

        img = Image.open(BytesIO(info[5])).resize((100, 100), Image.BILINEAR)
        self.worker.photo = ImageTk.PhotoImage(img)
        self.worker.photo_label.config(image=self.worker.photo)

        self.worker.post_text.insert(1.0, f"{info[6]}")

        self.worker.name_text.config(state=DISABLED)
        self.worker.birth_date_text.config(state=DISABLED)
        self.worker.post_text.config(state=DISABLED)

    def more_info(self):
        self.view.create_tab('FullWorkerInfo', self.worker.id, self.worker.notebook, self.worker)
        self.full_worker_info[self.worker.id] = FullWorkerInfoController(self, self.model, self.view, self.worker.id)

    def delete_worker(self):
        self.model.delete_worker(self.worker.id)
        self.full_worker_info.clear()
        self.all_workers_controller.workers_controllers.pop(str(self.worker.id))
        self.worker.destroy()

    def open_projects(self):
        self.view.create_tab('OpenProjects', self.worker.id, self.worker.notebook, self.worker)
        self.worker_projects[self.worker.id] = WorkerProjectsController(self, self.model, self.view, self.worker.id)
