from MVC.Controllers.all_workers import AllWorkersController
from MVC.Controllers.worker import WorkerController

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno


class UnitWorkersController(AllWorkersController):
    def __init__(self, main_controller, model, view, unit_name):
        self.unit_name = unit_name
        super().__init__(main_controller, model, view)

    def _initialize_tab(self):
        self.view.tabs['UnitWorkers'] = self.view.create_tab('UnitWorkers', self.view.app.notebook, self.unit_name)
        self.tab = self.view.tabs['UnitWorkers']
        self.tab.add_worker_button.config(command=self.add_worker)
        self.tab.close_button.config(command=self.close_tab)
        self.tab.add_tab()
        self.tab.sort_lastname.config(command=lambda: self.sort_by('LastName'))
        self.tab.sort_firstname.config(command=lambda: self.sort_by('FirstName'))

    def _get_all_workers(self, sort_by='LastName', reverse=False):
        for i in self.model.get_unit_workers(self.unit_name, sort_by, reverse):
            self.view.create_tab(
                'Worker',
                i,
                i,
                self.tab.frame.interior,
                self.tab.notebook
            )
            self.workers_controllers[f'{i}'] = WorkerController(self, self.model, self.view, i)

    def add_worker(self):
        add_worker_win = Toplevel(self.view.app)
        add_worker_win.title('Додайте робітників')

        workers_lf = LabelFrame(add_worker_win, text='Виберіть робітників')
        workers_lf.pack(padx=5, pady=5)
        workers_listbox = Listbox(workers_lf, selectmode=MULTIPLE, height=20, width=60, font=14)
        workers_listbox.pack(padx=5, pady=5)

        not_unit_workers = self.model.get_not_unit_workers(self.unit_name)
        not_unit_workers_ids = []

        for worker in not_unit_workers:
            not_unit_workers_ids.append(worker[0])
            workers_listbox.insert('end', " ".join(worker[1:]))

        def on_ok():
            for i in workers_listbox.curselection():
                if 'знаходиться у підрозділі' in workers_listbox.get(i).split(' (')[1][:-1]:
                    ans = askyesno("Увага", f"{workers_listbox.get(i).split(' (')[0]} вже знаходиться в "
                                            f"підрозділі. Бажаєте змінити його підрозділ?")
                    if ans:
                        self.model.set_worker_unit(not_unit_workers_ids[i], self.unit_name)
                else:
                    self.model.set_worker_unit(not_unit_workers_ids[i], self.unit_name)
            self.view.worker_tabs.clear()
            self.workers_controllers.clear()
            for i in self.tab.frame.interior.winfo_children():
                i.destroy()
            self._get_all_workers()
            add_worker_win.destroy()

        def on_cancel():
            add_worker_win.destroy()

        buttons_frame = ttk.Frame(workers_lf)
        buttons_frame.pack(padx=5, pady=5, side=RIGHT)
        ok_button = ttk.Button(buttons_frame, text="Ок", command=on_ok)
        ok_button.pack(padx=5, pady=5, side=LEFT)
        cancel_button = ttk.Button(buttons_frame, text="Скасувати", command=on_cancel)
        cancel_button.pack(padx=5, pady=5, side=LEFT)
