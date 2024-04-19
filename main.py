from tkinter import *
import tkinter.ttk as ttk

from PIL import Image, ImageTk

from io import BytesIO

import db_module as db


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Відділ кадрів')

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.notebook = ttk.Notebook(self)

        self.window1 = ttk.Frame(self.notebook)

        self.add_worker_button = ttk.Button(self.window1, text='Додати', command=self.add_worker)
        self.add_worker_button.pack(anchor=W, padx=5, pady=5)

        self.frame = VerticalScrolledFrame(self.window1)
        self.frame.pack(expand=True, fill=BOTH)

        self.notebook.add(self.window1, text="Workers list")
        self.notebook.pack(padx=5, pady=5, expand=True)

        self.get_all_workers()

    def close_app(self):
        db.connection.close()
        self.destroy()

    def get_all_workers(self):
        workers = db.get_all_workers()
        for x in workers:
            worker = Worker(self.frame.interior, self.notebook)
            worker.name_text.config(state=NORMAL)
            worker.email_text.config(state=NORMAL)
            worker.birth_date_text.config(state=NORMAL)
            worker.post_text.config(state=NORMAL)

            worker.id = x[0]
            worker.name_text.insert(1.0, f"{x[1]} {x[2]} {x[3]}")
            worker.email_text.insert(1.0, f"{x[4]}")
            worker.birth_date_text.insert(1.0, f"{x[5]}")
            worker.post_text.insert(1.0, f"{x[6]}")

            img = Image.open(BytesIO(x[7]))
            worker.photo = ImageTk.PhotoImage(img)
            worker.photo_label.config(image=worker.photo)

            worker.name_text.config(state=DISABLED)
            worker.birth_date_text.config(state=DISABLED)
            worker.post_text.config(state=DISABLED)

    def add_worker(self):
        # worker = Worker(self.frame.interior)
        # worker_id = self.save_worker_to_db(worker)
        # worker.id = worker_id
        ...

    # def save_worker_to_db(self, worker):
    #     ...


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        v_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, width=500, height=500, yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        v_scrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

    def _configure_interior(self, event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())


class Worker(ttk.Frame):
    def __init__(self, parent, notebook):
        super().__init__(parent)

        self.notebook = notebook

        self.id = None

        self.info_page = None

        self.config(relief=RIDGE, borderwidth=2)
        self.pack(padx=5, pady=5, anchor=W)

        self.photo = None
        self.photo_frame = ttk.Frame(self, relief=RIDGE, borderwidth=2)
        self.photo_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack()

        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.name_label = ttk.Label(self.info_frame, text="ПІБ:")
        self.name_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.email_label = ttk.Label(self.info_frame, text="Email:")
        self.email_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.birth_date_label = ttk.Label(self.info_frame, text="Дата народження:")
        self.birth_date_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.post_label = ttk.Label(self.info_frame, text="Посада:")
        self.post_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.name_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.name_text.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.email_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.email_text.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.birth_date_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.birth_date_text.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        self.post_text = Text(self.info_frame, state=DISABLED, height=1, width=35)
        self.post_text.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5)

        self.button_view = ttk.Button(self.buttons_frame, text="Докладніше", command=self.more_info)
        self.button_view.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.button_delete = ttk.Button(self.buttons_frame, text="Видалити", command=self.delete)
        self.button_delete.grid(row=2, column=1, sticky=W, padx=5, pady=5)

    def more_info(self):
        self.info_page = FullWorkerInfo(self.notebook, self.name_text.get(1.0, END)[:-1], self.id)

    def delete(self):
        db.delete_worker(self.id)
        self.destroy()


class FullWorkerInfo:
    def __init__(self, notebook, name, worker_id):
        self.id = worker_id

        self.notebook = notebook
        self.mainFrame = ttk.Frame(notebook)

        self.photo = None
        self.photo_frame = ttk.Frame(self.mainFrame, relief=RIDGE, borderwidth=2)
        self.photo_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack()

        self.info_frame = ttk.Frame(self.mainFrame)
        self.info_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.lastName_Label = ttk.Label(self.info_frame, text="Прізвище: ")
        self.lastName_Label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.firstName_Label = ttk.Label(self.info_frame, text="Ім'я: ")
        self.firstName_Label.grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.patronymic_Label = ttk.Label(self.info_frame, text="По-батькові: ")
        self.patronymic_Label.grid(row=0, column=4, sticky=W, padx=5, pady=5)
        self.email_Label = ttk.Label(self.info_frame, text="Email: ")
        self.email_Label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.birthDate_Label = ttk.Label(self.info_frame, text="Дата народження: ")
        self.birthDate_Label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.post_Label = ttk.Label(self.info_frame, text="Посада: ")
        self.post_Label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.birthPlace_Label = ttk.Label(self.info_frame, text="Місце народження: ")
        self.birthPlace_Label.grid(row=2, column=2, sticky=W, padx=5, pady=5)
        self.educationInfo_Label = ttk.Label(self.info_frame, text="Інформація про освіту: ")
        self.educationInfo_Label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.languageInfo_Label = ttk.Label(self.info_frame, text="Володіння іноземними мовами: ")
        self.languageInfo_Label.grid(row=5, column=0, sticky=W, padx=5, pady=5)

        self.lastName_Entry = Entry(self.info_frame, width=15)
        self.lastName_Entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.firstName_Entry = Entry(self.info_frame, width=15)
        self.firstName_Entry.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        self.patronymic_Entry = Entry(self.info_frame, width=15)
        self.patronymic_Entry.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        self.email_Entry = Entry(self.info_frame, width=15)
        self.email_Entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.birthDate_Entry = Entry(self.info_frame, width=15)
        self.birthDate_Entry.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        self.post_Entry = Entry(self.info_frame, width=15)
        self.post_Entry.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        self.birthPlace_Entry = Entry(self.info_frame, width=15)
        self.birthPlace_Entry.grid(row=2, column=3, sticky=W, padx=5, pady=5)
        self.educationInfo_Entry = Entry(self.info_frame, width=15)
        self.educationInfo_Entry.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        self.languageInfo_Entry = Entry(self.info_frame, width=15)
        self.languageInfo_Entry.grid(row=5, column=1, sticky=W, padx=5, pady=5)

        self.closeTab_Button = ttk.Button(self.mainFrame, text="Зберегти та закрити вкладку", command=self.close_tab)
        self.closeTab_Button.pack()

        notebook.insert("end", self.mainFrame, text=name)

        self.get_info_from_db(self.id)

    def get_info_from_db(self, worker_id):
        info = db.get_worker_full_info(worker_id)
        self.lastName_Entry.insert(END, str(info[0][1]))
        self.firstName_Entry.insert(END, str(info[0][2]))
        self.patronymic_Entry.insert(END, str(info[0][3]))
        self.email_Entry.insert(END, str(info[0][4]))
        self.birthDate_Entry.insert(END, str(info[0][5]))
        self.post_Entry.insert(END, str(info[0][6]))

        img = Image.open(BytesIO(info[0][7]))
        self.photo = ImageTk.PhotoImage(img)
        self.photo_label.config(image=self.photo)

        self.birthPlace_Entry.insert(END, str(info[0][8]))
        self.educationInfo_Entry.insert(END, str(info[0][9]))
        self.languageInfo_Entry.insert(END, str(info[0][10]))

    def close_tab(self):
        self.notebook.forget(self.mainFrame)


# class AddWorkerWindow(Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#
#         self.title("Додати нового робітника")


def main():
    hrd = App()
    hrd.mainloop()


if __name__ == '__main__':
    main()
