from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


class FullWorkerInfoController:
    def __init__(self, model, view, worker_id):
        self.model = model
        self.view = view
        self.full_worker_info = self.view.full_info_tabs[worker_id]
        self.full_worker_info.closeTab_Button.config(command=self.close_tab)
        self.get_info_from_db(worker_id)

    def get_info_from_db(self, worker_id):
        info = self.model.get_worker_full_info(worker_id)

        for i in range(len(info[0])):
            if i < 4:
                if info[0][i] is not None:
                    self.full_worker_info.entries_general[i].insert(END, info[0][i])
            elif i == 4:
                img = Image.open(BytesIO(info[0][i]))
                self.full_worker_info.photo = ImageTk.PhotoImage(img)
                self.full_worker_info.photo_label.config(image=self.full_worker_info.photo)
            elif i > 4:
                if info[0][i] is not None:
                    self.full_worker_info.entries_general[i - 1].insert(END, info[0][i])

        for row in info[1]:
            self.full_worker_info.tables_firstSection[0].insert(parent='', index=END, values=row[1:])

        for row in info[1]:
            self.full_worker_info.tables_firstSection[1].insert(parent='', index=END, values=row[4:])

        for row in range(len(info[2])):
            if info[2][row][1] == 1:
                self.full_worker_info.graduateSchool_Entry.insert(END, "X")
                self.full_worker_info.graduateSchool_Entry.associated_row = row
            elif info[2][row][1] == 2:
                self.full_worker_info.adjunct_Entry.insert(END, "X")
                self.full_worker_info.adjunct_Entry.associated_row = row
            elif info[2][row][1] == 3:
                self.full_worker_info.doctoralStudies_Entry.insert(END, "X")
                self.full_worker_info.doctoralStudies_Entry.associated_row = row
            self.full_worker_info.tables_firstSection[2].insert(parent='', index=END, values=info[2][row][2:])

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
        self.model.update_info(self.full_worker_info.id, info)

        self.full_worker_info.worker.name_text.config(state=NORMAL)
        self.full_worker_info.worker.email_text.config(state=NORMAL)
        self.full_worker_info.worker.birth_date_text.config(state=NORMAL)
        self.full_worker_info.worker.post_text.config(state=NORMAL)

        self.full_worker_info.worker.name_text.delete(1.0, END)
        self.full_worker_info.worker.birth_date_text.delete(1.0, END)

        self.full_worker_info.worker.name_text.insert(END, f"{info[0]} {info[1]} {info[2]}")
        self.full_worker_info.worker.birth_date_text.insert(END, info[3])

        self.full_worker_info.worker.name_text.config(state=DISABLED)
        self.full_worker_info.worker.email_text.config(state=DISABLED)
        self.full_worker_info.worker.birth_date_text.config(state=DISABLED)
        self.full_worker_info.worker.post_text.config(state=DISABLED)

        def get_all_rows(table):
            output = []
            n = 1
            try:
                while True:
                    output.append(table.item(f'I00{n}').get('values'))
                    n += 1
            except TclError:
                return output

        for t in range(len(self.full_worker_info.tables_firstSection)):
            data = []
            if t == 0:
                for row in zip(get_all_rows(self.full_worker_info.tables_firstSection[t]),
                               get_all_rows(self.full_worker_info.tables_firstSection[t+1])):
                    data.append(row[0])
            elif t == 1:
                continue
            elif t == 2:
                check_box = [self.full_worker_info.graduateSchool_Entry.associated_row,
                             self.full_worker_info.adjunct_Entry.associated_row,
                             self.full_worker_info.doctoralStudies_Entry.associated_row]
                for row in get_all_rows(self.full_worker_info.tables_firstSection[t]):
                    data.append(row)
                for i in range(len(check_box)):
                    if check_box[i] is not None:
                        data[check_box[i]] = [i + 1] + data[check_box[i]]
            else:
                for row in get_all_rows(self.full_worker_info.tables_firstSection[t]):
                    data.append(row)
            self.model.update_table(self.full_worker_info.id, 0, t, data)

        for t in range(len(self.full_worker_info.tables_other)):
            data = []
            for row in get_all_rows(self.full_worker_info.tables_other[t]):
                data.append(row)
            self.model.update_table(self.full_worker_info.id, 1, t, data)

        self.full_worker_info.notebook.forget(self.full_worker_info.mainFrame)