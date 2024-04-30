from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

from MVC.Controllers.full_worker_info import FullWorkerInfoController


class WorkerController:
    def __init__(self, model, view, worker_id):
        self.model = model
        self.view = view
        self.worker = self.view.worker_tabs[worker_id]
        self.worker.button_view.config(command=self.more_info)
        self.worker.button_delete.config(command=self.delete)
        self.full_worker_infos = {}
        self.get_info()

    def get_info(self):
        info = self.model.get_worker_info(self.worker.id)
        self.worker.name_text.config(state=NORMAL)
        self.worker.email_text.config(state=NORMAL)
        self.worker.birth_date_text.config(state=NORMAL)
        self.worker.post_text.config(state=NORMAL)

        self.worker.name_text.insert(1.0, f"{info[1]} {info[2]} {info[3]}")
        self.worker.email_text.insert(1.0, f"{info[4]}")
        self.worker.birth_date_text.insert(1.0, f"{info[5]}")

        img = Image.open(BytesIO(info[6]))
        self.worker.photo = ImageTk.PhotoImage(img)
        self.worker.photo_label.config(image=self.worker.photo)

        self.worker.post_text.insert(1.0, f"{info[7]}")

        self.worker.name_text.config(state=DISABLED)
        self.worker.email_text.config(state=DISABLED)
        self.worker.birth_date_text.config(state=DISABLED)
        self.worker.post_text.config(state=DISABLED)

    def more_info(self):
        self.view.create_tab(self.worker.id, 'FullWorkerInfo', self.worker.notebook, self.worker)
        self.full_worker_infos[self.worker.id] = FullWorkerInfoController(self.model, self.view, self.worker.id)

    def delete(self):
        # db.delete_worker(self.id)
        # self.destroy()
        pass
