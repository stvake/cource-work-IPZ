from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter.messagebox import showwarning

from MVC.Controllers.worker import WorkerController


class AddNewWorkerController:
    def __init__(self, main_controller, model, view):
        self.main_controller = main_controller
        self.model = model
        self.view = view
        self.tab = self.view.tabs['AddNewWorker']
        self.tab.add_photo_button.config(command=self.add_photo)
        self.tab.saveButton.config(command=self.save_worker)
        self.photo_path = None
        self.id = None
        self.ready_to_save = 1

    def add_photo(self):
        p = askopenfilename()
        if len(p) != 0:
            self.photo_path = p
            self.tab.photo = PhotoImage(file=p)
            self.tab.image_label.config(text='', image=self.tab.photo)

    def save_worker(self):
        self.id = self.model.create_new_worker()
        with open(self.photo_path, 'rb') as file:
            image_data = file.read()
            self.model.upload_image(self.id, image_data)
            info = [i.get() for i in self.tab.entries_general]
            info.insert(4, image_data)
            mil_info = [i.get() for i in self.tab.entries_secondSection]
            self.model.update_info(self.id, info, mil_info)

        def get_all_rows(table):
            output = []
            n = 1
            try:
                while True:
                    output.append(table.item(f'I00{n}').get('values'))
                    n += 1
            except TclError:
                return output

        for t in range(len(self.tab.tables_firstSection)):
            data = []
            if t == 0:
                for row in zip(get_all_rows(self.tab.tables_firstSection[t]),
                               get_all_rows(self.tab.tables_firstSection[t + 1])):
                    data.append(row[0] + row[1])
            elif t == 1:
                continue
            else:
                for row in get_all_rows(self.tab.tables_firstSection[t]):
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
                self.model.update_table(self.id, 0, t, data)
                self.ready_to_save = 1

        for t in range(len(self.tab.tables_other)):
            data = []
            for row in get_all_rows(self.tab.tables_other[t]):
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
                self.model.update_table(self.id, 1, t, data)
                self.ready_to_save = 1

        if self.ready_to_save:
            self.view.create_tab(
                self.id,
                'Worker',
                self.id,
                self.view.tabs['Workers'].frame.interior,
                self.view.tabs['Workers'].notebook
            )
            self.main_controller.all_workers_controller.workers_controllers[self.id] = (
                WorkerController(self.main_controller.all_workers_controller, self.model, self.view, self.id))
            self.tab.notebook.forget(self.tab.mainFrame)
