from tkinter import *
from tkinter.messagebox import showwarning
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from io import BytesIO


class FullWorkerInfoController:
    def __init__(self, worker_controller, model, view, worker_id):
        self.worker_controller = worker_controller
        self.model = model
        self.view = view
        self.worker_id = worker_id
        self.tab = self.view.full_info_tabs[self.worker_id]
        self.tab.add_photo_button.config(command=self.add_photo)
        self.tab.closeTab_Button.config(command=self.close_tab)
        self.tab.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.ready_to_save = 1
        self.image_data = None
        self.photo_path = None
        self.get_info_from_db(self.worker_id)

    def add_photo(self):
        filetypes = [("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        p = askopenfilename(filetypes=filetypes)
        if len(p) != 0:
            self.photo_path = p
            self.tab.photo = ImageTk.PhotoImage(Image.open(p).resize((100, 100), Image.BILINEAR))
            self.tab.photo_label.config(image=self.tab.photo)
            with open(p, 'rb') as f:
                self.image_data = f.read()

    def refresh_workers(self):
        for i in self.view.tabs['Workers'].frame.interior.winfo_children():
            i.destroy()
        self.worker_controller.all_workers_controller.refresh()

    def get_info_from_db(self, worker_id):
        info = self.model.get_worker_full_info(worker_id)

        for i in range(len(info[0])):
            if i < 4:
                if info[0][i] is not None:
                    self.tab.entries_general[i].insert(END, info[0][i])
            elif i == 4:
                self.image_data = info[0][i]
                img = Image.open(BytesIO(self.image_data)).resize((100, 100), Image.BILINEAR)
                self.tab.photo = ImageTk.PhotoImage(img)
                self.tab.photo_label.config(image=self.tab.photo)
            elif i > 4:
                if info[0][i] is not None:
                    self.tab.entries_general[i - 1].insert(END, info[0][i])
        for row in info[1]:
            self.tab.tables_firstSection[0].insert(parent='', index=END, values=row[1:4])

        for row in info[1]:
            self.tab.tables_firstSection[1].insert(parent='', index=END, values=row[4:])

        for row in range(len(info[2])):
            if info[2][row][-1] == 'Аспірантура':
                self.tab.graduateSchool_Entry.insert(END, "X")
                self.tab.graduateSchool_Entry.associated_row = row
            elif info[2][row][-1] == "Ад'юнктура" or info[2][row][-1] == "Ад'юнктура":
                self.tab.adjunct_Entry.insert(END, "X")
                self.tab.adjunct_Entry.associated_row = row
            elif info[2][row][-1] == 'Докторантура':
                self.tab.doctoralStudies_Entry.insert(END, "X")
                self.tab.doctoralStudies_Entry.associated_row = row
            self.tab.tables_firstSection[2].insert(parent='', index=END, values=info[2][row][1:])

        for row in info[3]:
            self.tab.tables_firstSection[3].insert(parent='', index=END, values=row[1:])

        for i in range(len(info[4])):
            if info[4][i] is not None:
                self.tab.entries_secondSection[i].insert(END, info[4][i])

        for i in range(len(self.tab.tables_other)):
            for row in info[5 + i]:
                self.tab.tables_other[i].insert(parent='', index=END, values=row[1:])

    def close_tab(self):
        info = [i.get() for i in self.tab.entries_general]
        info.insert(4, self.image_data)
        mil_info = [i.get() for i in self.tab.entries_secondSection]

        if self.model.update_info(self.tab.id, info, mil_info):
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
                if self.model.update_table(self.tab.id, 0, t, data):
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
                    return
            else:
                if self.model.update_table(self.tab.id, 1, t, data):
                    showwarning("Зауваження", "Правильно заповніть поля.")
                    return
                self.ready_to_save = 1

        if self.ready_to_save:
            self.refresh_workers()
            self.worker_controller.full_worker_info.pop(self.worker_id)
            self.tab.notebook.forget(self.tab.mainFrame)

    def close_tab_without_save(self):
        self.worker_controller.full_worker_info.pop(self.worker_id)
        self.tab.notebook.forget(self.tab.mainFrame)
