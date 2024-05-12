from tkinter import *
from tkinter.messagebox import showwarning
from PIL import Image, ImageTk
from io import BytesIO


class FullWorkerInfoController:
    def __init__(self, worker_controller, model, view, worker_id):
        self.worker_controller = worker_controller
        self.model = model
        self.view = view
        self.worker_id = worker_id
        self.full_worker_info = self.view.full_info_tabs[self.worker_id]
        self.full_worker_info.closeTab_Button.config(command=self.close_tab)
        self.full_worker_info.closeTabWithoutSave_Button.config(command=self.close_tab_without_save)
        self.ready_to_save = 1
        self.image_data = None
        self.get_info_from_db(self.worker_id)

    def get_info_from_db(self, worker_id):
        info = self.model.get_worker_full_info(worker_id)

        for i in range(len(info[0])):
            if i < 4:
                if info[0][i] is not None:
                    self.full_worker_info.entries_general[i].insert(END, info[0][i])
            elif i == 4:
                self.image_data = info[0][i]
                img = Image.open(BytesIO(self.image_data))
                self.full_worker_info.photo = ImageTk.PhotoImage(img)
                self.full_worker_info.photo_label.config(image=self.full_worker_info.photo)
            elif i > 4:
                if info[0][i] is not None:
                    self.full_worker_info.entries_general[i - 1].insert(END, info[0][i])
        for row in info[1]:
            self.full_worker_info.tables_firstSection[0].insert(parent='', index=END, values=row[1:4])

        for row in info[1]:
            self.full_worker_info.tables_firstSection[1].insert(parent='', index=END, values=row[4:])

        for row in range(len(info[2])):
            if info[2][row][-1] == 'Аспірантура':
                self.full_worker_info.graduateSchool_Entry.insert(END, "X")
                self.full_worker_info.graduateSchool_Entry.associated_row = row
            elif info[2][row][-1] == "Ад'юнктура" or info[2][row][-1] == "Ад'юнктура":
                self.full_worker_info.adjunct_Entry.insert(END, "X")
                self.full_worker_info.adjunct_Entry.associated_row = row
            elif info[2][row][-1] == 'Докторантура':
                self.full_worker_info.doctoralStudies_Entry.insert(END, "X")
                self.full_worker_info.doctoralStudies_Entry.associated_row = row
            self.full_worker_info.tables_firstSection[2].insert(parent='', index=END, values=info[2][row][1:])

        for row in info[3]:
            self.full_worker_info.tables_firstSection[3].insert(parent='', index=END, values=row[1:])

        for i in range(len(info[4])):
            if info[4][i] is not None:
                self.full_worker_info.entries_secondSection[i].insert(END, info[4][i])

        for i in range(len(self.full_worker_info.tables_other)):
            for row in info[5 + i]:
                self.full_worker_info.tables_other[i].insert(parent='', index=END, values=row[1:])

    def close_tab(self):
        info = [i.get() for i in self.full_worker_info.entries_general]
        info.insert(4, self.image_data)
        mil_info = [i.get() for i in self.full_worker_info.entries_secondSection]

        if self.model.update_info(self.full_worker_info.id, info, mil_info):
            showwarning("Зауваження", "Правильно заповніть поля.")
            return

        self.full_worker_info.worker.name_text.config(state=NORMAL)
        self.full_worker_info.worker.birth_date_text.config(state=NORMAL)
        self.full_worker_info.worker.post_text.config(state=NORMAL)

        self.full_worker_info.worker.name_text.delete(1.0, END)
        self.full_worker_info.worker.birth_date_text.delete(1.0, END)
        self.full_worker_info.worker.post_text.delete(1.0, END)

        self.full_worker_info.worker.name_text.insert(END, f"{info[0]} {info[1]} {info[2]}")
        self.full_worker_info.worker.birth_date_text.insert(END, info[3])
        indexes = self.full_worker_info.appointment_table.get_children()
        values = []
        for i in indexes:
            values.append(self.full_worker_info.appointment_table.item(i).get('values'))
        sorted_values = sorted(values, key=lambda x: x[0])
        self.full_worker_info.worker.post_text.insert(END, sorted_values[-1][2])

        self.full_worker_info.worker.name_text.config(state=DISABLED)
        self.full_worker_info.worker.birth_date_text.config(state=DISABLED)
        self.full_worker_info.worker.post_text.config(state=DISABLED)

        def get_all_rows(table):
            output = []
            for line in table.get_children():
                output.append(table.item(line).get('values'))
            return output

        for t in range(len(self.full_worker_info.tables_firstSection)):
            data = []
            if t == 0:
                for row in zip(get_all_rows(self.full_worker_info.tables_firstSection[t]),
                               get_all_rows(self.full_worker_info.tables_firstSection[t+1])):
                    data.append(row[0] + row[1])
            elif t == 1:
                continue
            else:
                for row in get_all_rows(self.full_worker_info.tables_firstSection[t]):
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
                if self.model.update_table(self.full_worker_info.id, 0, t, data):
                    showwarning("Зауваження", "Правильно заповніть поля.")
                    return
                self.ready_to_save = 1

        for t in range(len(self.full_worker_info.tables_other)):
            data = []
            for row in get_all_rows(self.full_worker_info.tables_other[t]):
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
                if self.model.update_table(self.full_worker_info.id, 1, t, data):
                    showwarning("Зауваження", "Правильно заповніть поля.")
                    return
                self.ready_to_save = 1

        if self.ready_to_save:
            self.worker_controller.full_worker_info.pop(self.worker_id)
            self.full_worker_info.notebook.forget(self.full_worker_info.mainFrame)

    def close_tab_without_save(self):
        self.worker_controller.full_worker_info.pop(self.worker_id)
        self.full_worker_info.notebook.forget(self.full_worker_info.mainFrame)
