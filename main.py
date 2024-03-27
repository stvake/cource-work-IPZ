from tkinter import *
import tkinter.ttk as ttk

import db_module as db


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Відділ кадрів')

        self.protocol("WM_DELETE_WINDOW", self.close_app)

        self.add_worker_button = ttk.Button(self, text='Додати', command=self.add_worker)
        self.add_worker_button.pack(anchor=W, padx=5, pady=5)

        self.frame = VerticalScrolledFrame(self)
        self.frame.pack(expand=True, fill=BOTH)

        self.get_all_workers()

    def close_app(self):
        db.connection.close()
        self.destroy()

    def get_all_workers(self):
        workers = db.get_all_workers()
        for x in workers:
            worker = Worker(self.frame.interior)
            worker.name_text.config(state=NORMAL)
            worker.email_text.config(state=NORMAL)
            worker.birth_date_text.config(state=NORMAL)
            worker.post_text.config(state=NORMAL)

            worker.id = x[0]
            worker.name_text.insert(1.0, f"{x[1]} {x[2]} {x[3]}")
            worker.email_text.insert(1.0, f"{x[4]}")
            worker.birth_date_text.insert(1.0, f"{x[5]}")
            worker.post_text.insert(1.0, f"{x[6]}")
            worker.photo = PhotoImage(file=x[7])
            worker.photo_label.config(image=worker.photo)

            worker.name_text.config(state=DISABLED)
            worker.birth_date_text.config(state=DISABLED)
            worker.post_text.config(state=DISABLED)

    def add_worker(self):
        worker = Worker(self.frame.interior)
        # worker_id = self.save_worker_to_db(worker)
        # worker.id = worker_id

    def save_worker_to_db(self, worker):
        ...


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                             width=500, height=500,
                             yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)

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
    def __init__(self, parent):
        super().__init__(parent)

        self.id = None

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
        # open tab with full worker info
        ...

    def delete(self):
        db.delete_worker(self.id)
        self.destroy()


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
