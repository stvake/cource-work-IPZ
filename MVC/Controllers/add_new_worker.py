from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.messagebox import showwarning
from PIL import Image, ImageTk


class AddNewWorkerController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.view.tabs['AddNewWorker'] = self.view.create_tab('AddNewWorker')
        self.tab = self.view.tabs['AddNewWorker']
        self.tab.add_photo_button.config(command=self.add_photo)
        self.tab.saveButton.config(command=self.save_worker)
        self.tab.cancelButton.config(command=self.cancel)
        self.photo_path = None
        self.id = None
        self.ready_to_save = 1

    def add_photo(self):
        filetypes = [("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        p = askopenfilename(filetypes=filetypes)
        if len(p) != 0:
            self.photo_path = p
            self.tab.photo = ImageTk.PhotoImage(Image.open(p).resize((100, 100), Image.BILINEAR))
            self.tab.image_label.config(text='', image=self.tab.photo)

    def refresh_workers(self):
        self.main_controller.all_workers_controller.refresh()

    def save_worker(self):
        if not self.photo_path:
            self.ready_to_save = 0
            showwarning("Зауваження", "Завантажте фото працівника.")
            return
        else:
            self.id = self.model.create_new_worker()
            with open(self.photo_path, 'rb') as file:
                image_data = file.read()
                self.model.upload_image(self.id, image_data)
                info = [i.get() for i in self.tab.entries_general]
                info.insert(4, image_data)
                mil_info = [i.get() for i in self.tab.entries_secondSection]
                if self.model.update_info(self.id, info, mil_info):
                    showwarning("Зауваження", "Правильно заповніть поля.")
                    return

            for t in range(len(self.tab.tables_firstSection)):
                data = []
                if t == 0:
                    for row in zip(self.tab.tables_firstSection[t].get_all_rows(),
                                   self.tab.tables_firstSection[t + 1].get_all_rows()):
                        data.append(row[0] + row[1])
                elif t == 1:
                    continue
                else:
                    for row in self.tab.tables_firstSection[t].get_all_rows():
                        data.append(row)

                quantity_of_empty_elements = 0
                for d in data:
                    if '' in d and d.count('') != len(d):
                        quantity_of_empty_elements += 1

                if quantity_of_empty_elements != 0:
                    if self.ready_to_save:
                        showwarning("Зауваження", "Правильно заповніть поля.")
                        self.ready_to_save = 0
                        return
                else:
                    if self.model.update_table(self.id, 0, t, data):
                        showwarning("Зауваження", "Правильно заповніть поля.")
                        return
                    self.ready_to_save = 1

            for t in range(len(self.tab.tables_other)):
                data = []
                for row in self.tab.tables_other[t].get_all_rows():
                    data.append(row)

                quantity_of_empty_elements = 0
                for d in data:
                    if '' in d and d.count('') != len(d):
                        quantity_of_empty_elements += 1

                if quantity_of_empty_elements != 0:
                    if self.ready_to_save:
                        showwarning("Зауваження", "Правильно заповніть поля.")
                        self.ready_to_save = 0
                else:
                    if self.model.update_table(self.id, 1, t, data):
                        showwarning("Зауваження", "Правильно заповніть поля.")
                        return
                    self.ready_to_save = 1

            if self.ready_to_save:
                self.refresh_workers()
                self.tab.notebook.forget(self.tab.mainFrame)

    def cancel(self):
        self.main_controller.add_new_worker_controller = None
        self.tab.notebook.forget(self.tab.mainFrame)
