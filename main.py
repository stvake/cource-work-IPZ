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

        self.main_tab = ttk.Frame(self.notebook)

        self.add_worker_button = ttk.Button(self.main_tab, text='Додати', command=self.add_worker)
        self.add_worker_button.pack(anchor=W, padx=5, pady=5)

        self.frame = VerticalScrolledFrame(self.main_tab)
        self.frame.pack(expand=True, fill=BOTH)

        self.notebook.add(self.main_tab, text="Список робітників")
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
        self.canvas = Canvas(self, bd=0, highlightthickness=0, width=500, height=750, yscrollcommand=v_scrollbar.set)
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
        for x in self.get_all_widgets(self):
            x.bind('<MouseWheel>', self._on_mousewheel)

        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

    def get_all_widgets(self, parent):
        all_widgets = [parent]
        for child in parent.winfo_children():
            all_widgets.extend(self.get_all_widgets(child))
        return all_widgets

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class Worker(ttk.Frame):
    def __init__(self, parent, notebook):
        super().__init__(parent)

        self.notebook = notebook

        self.id = None

        self.info_page = None

        self.config(relief=GROOVE)
        self.pack(padx=5, pady=5, anchor=W)

        self.photo = None
        self.photo_frame = ttk.Frame(self, relief=GROOVE)
        self.photo_frame.pack(side=LEFT, anchor=W, padx=5, pady=5)

        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack(padx=2, pady=2)

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

        self.name = name

        self.notebook = notebook
        self.mainFrame = ttk.Frame(notebook)

        self.mainScrolledFrame = VerticalScrolledFrame(self.mainFrame)
        self.mainScrolledFrame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.photo = None
        self.photo_frame = ttk.Frame(self.mainFrame, relief=GROOVE)
        self.photo_frame.pack(side=LEFT, anchor=NW, padx=5, pady=10)

        self.photo_label = ttk.Label(self.photo_frame)
        self.photo_label.pack(padx=2, pady=2)

        self.docsTab = None

        # Frames
        self.firstSection = ttk.Labelframe(self.mainScrolledFrame.interior, text="І. ЗАГАЛЬНІ ВІДОМОСТІ")
        self.firstSection.pack(fill=BOTH, padx=5, pady=5)
        self.secondSection = ttk.Labelframe(self.mainScrolledFrame.interior, text="ІІ. ВІДОМОСТІ ПРО ВІЙСЬКОВИЙ ОБЛІК")
        self.secondSection.pack(fill=BOTH, padx=5, pady=5)
        self.thirdSection = ttk.Labelframe(self.mainScrolledFrame.interior,
                                           text="ІІІ. ПРОФЕСІЙНА ОСВІТА НА ВИРОБНИЦТВІ "
                                                "(ЗА РАХУНОК ""ПІДПРИЄМСТВА - РОБОТОДАВЦЯ)")
        self.thirdSection.pack(fill=BOTH, padx=5, pady=5)
        self.fourthSection = ttk.Labelframe(self.mainScrolledFrame.interior, text="IV. ПРИЗНАЧЕННЯ І ПЕРЕВЕДЕННЯ")
        self.fourthSection.pack(fill=BOTH, padx=5, pady=5)
        self.fifthSection = ttk.Labelframe(self.mainScrolledFrame.interior, text="V. ВІДПУСТКИ")
        self.fifthSection.pack(fill=BOTH, padx=5, pady=5)

        # Labels
        self.generalInformation = ttk.Label()
        self.lastName_Label = ttk.Label(self.firstSection, text="Прізвище: ")
        self.lastName_Label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.firstName_Label = ttk.Label(self.firstSection, text="Ім'я: ")
        self.firstName_Label.grid(row=0, column=2, sticky=W, padx=5, pady=5)
        self.patronymic_Label = ttk.Label(self.firstSection, text="По-батькові: ")
        self.patronymic_Label.grid(row=0, column=4, sticky=W, padx=5, pady=5)
        self.birthDate_Label = ttk.Label(self.firstSection, text="Дата народження: ")
        self.birthDate_Label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.nationality_Label = ttk.Label(self.firstSection, text="Громадянство: ")
        self.nationality_Label.grid(row=1, column=2, sticky=W, padx=5, pady=5)
        self.education_Label = ttk.Label(self.firstSection, text="Освіта (базова загальна середня, "
                                                                 "повна загальна середня, професійно-технічна, "
                                                                 "базова вища, неповна вища, повна вища) ")
        self.education_Label.grid(row=2, column=0, columnspan=6, sticky=W, padx=5, pady=5)

        self.Postgraduate_Label = ttk.Label(self.firstSection, text="Післядипломна професійна підготовка: ")
        self.Postgraduate_Label.grid(row=6, column=0, columnspan=6, padx=5, pady=5, sticky=W)

        self.graduateSchool_Label = ttk.Label(self.firstSection, text="аспірантура: ")
        self.graduateSchool_Label.grid(row=7, column=0, padx=5, pady=5)
        self.adjunct_Label = ttk.Label(self.firstSection, text="ад'юнктура: ")
        self.adjunct_Label.grid(row=7, column=2, padx=5, pady=5)
        self.doctoralStudies_Label = ttk.Label(self.firstSection, text="докторантура: ")
        self.doctoralStudies_Label.grid(row=7, column=4, padx=5, pady=5)

        self.lastWork_Label = ttk.Label(self.firstSection, text="Останнє місце роботи ")
        self.lastWork_Label.grid(row=9, column=0, padx=5, pady=5, sticky=W)
        self.lastPost_Label = ttk.Label(self.firstSection, text="посада (професія) ")
        self.lastPost_Label.grid(row=9, column=2, padx=5, pady=5, sticky=W)

        self.workExpDate_Label = ttk.Label(self.firstSection, text="Стаж роботи станом на")
        self.workExpDate_Label.grid(row=10, column=0, padx=5, pady=5, sticky=W)
        self.workExpTotal_Label = ttk.Label(self.firstSection, text="Загальний")
        self.workExpTotal_Label.grid(row=10, column=1, padx=5, pady=5, sticky=E)
        self.workExpDays_Label = ttk.Label(self.firstSection, text="днів")
        self.workExpDays_Label.grid(row=10, column=2, padx=5, pady=5, sticky=E)
        self.workExpMonths_Label = ttk.Label(self.firstSection, text="місяців")
        self.workExpMonths_Label.grid(row=10, column=3, padx=5, pady=5)
        self.workExpYears_Label = ttk.Label(self.firstSection, text="років")
        self.workExpYears_Label.grid(row=10, column=4, padx=5, pady=5, sticky=W)

        self.workBonus_Label = ttk.Label(self.firstSection, text="Що дає право на надбавку за вислугу років")
        self.workBonus_Label.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky=E)
        self.workBonusDays_Label = ttk.Label(self.firstSection, text="днів")
        self.workBonusDays_Label.grid(row=11, column=2, padx=5, pady=5, sticky=E)
        self.workBonusMonths_Label = ttk.Label(self.firstSection, text="місяців")
        self.workBonusMonths_Label.grid(row=11, column=3, padx=5, pady=5)
        self.workBonusYears_Label = ttk.Label(self.firstSection, text="років")
        self.workBonusYears_Label.grid(row=11, column=4, padx=5, pady=5, sticky=W)

        self.workFire_Label = ttk.Label(self.firstSection, text="Дата та причина звільнення (скорочення штатів; за "
                                                                "власним бажанням, за прогул та інші порушення, "
                                                                "невідповідність посаді тощо)")
        self.workFire_Label.grid(row=12, columnspan=6, padx=5, pady=5, sticky=W)

        self.retire_Label = ttk.Label(self.firstSection, text="Відомості про отримання пенсії (у разі наявності "
                                                              "вказати вид пенсійних виплат згідно з чинним "
                                                              "законодавством)")
        self.retire_Label.grid(row=14, columnspan=6, padx=5, pady=5, sticky=W)

        self.family_Label = ttk.Label(self.firstSection, text="Родинний стан")
        self.family_Label.grid(row=16, column=0, padx=5, pady=5, sticky=W)

        self.residence_Label = ttk.Label(self.firstSection, text="Місце фактичного проживання (область, місто, район, "
                                                                 "вулиця, № будинку, квартири, номер контактного "
                                                                 "телефону, поштовий індекс)")
        self.residence_Label.grid(row=18, columnspan=6, padx=5, pady=5, sticky=W)

        self.registeredResidence_Label = ttk.Label(self.firstSection, text="Місце проживання за державною реєстрацією")
        self.registeredResidence_Label.grid(row=20, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        self.passport_Label = ttk.Label(self.firstSection, text="Паспорт:")
        self.passport_Label.grid(row=21, column=1, padx=5, pady=5, sticky=E)
        self.passportSeries_Label = ttk.Label(self.firstSection, text="серія")
        self.passportSeries_Label.grid(row=21, column=2, padx=5, pady=5, sticky=W)
        self.passportNumber_Label = ttk.Label(self.firstSection, text="№")
        self.passportNumber_Label.grid(row=21, column=3, padx=5, pady=5, sticky=W)
        self.passportIssuedBy_Label = ttk.Label(self.firstSection, text=", ким виданий")
        self.passportIssuedBy_Label.grid(row=21, column=4, padx=5, pady=5, sticky=W)
        self.passportDate_Label = ttk.Label(self.firstSection, text="дата видачі")
        self.passportDate_Label.grid(row=22, column=4, padx=5, pady=5)

        # Treeviews
        self.education_table1 = ttk.Treeview(self.firstSection, columns=('Name', 'Diploma', 'year'), show='headings',
                                             height=4)
        self.education_table1.heading('Name', text='Назва освітнього закладу')
        self.education_table1.heading('Diploma', text='Диплом (свідоцтво), серія, номер')
        self.education_table1.heading('year', text='Рік закінчення')
        self.education_table1.grid(row=4, column=0, columnspan=6, padx=5, sticky=NSEW)

        self.education_table2 = ttk.Treeview(self.firstSection, columns=('Spec', 'Cual', 'Form'), show='headings',
                                             height=4)
        self.education_table2.heading('Spec', text='Спеціальність (професія) за дипломом (свідоцтвом)')
        self.education_table2.heading('Cual', text='Кваліфікація за дипломом (свідоцтвом)')
        self.education_table2.heading('Form', text='Форма навчання')
        self.education_table2.grid(row=5, column=0, columnspan=6, padx=5, sticky=NSEW)

        self.education_table3 = ttk.Treeview(self.firstSection, columns=('Name', 'Diploma', 'year', 'degree'),
                                             show='headings', height=4)
        self.education_table3.heading('Name', text='Назва освітнього, наукового  закладу')
        self.education_table3.heading('Diploma', text='Диплом, номер, дата видачі')
        self.education_table3.heading('year', text='Рік закінчення')
        self.education_table3.heading('degree', text='Науковий ступінь, учене звання')
        self.education_table3.grid(row=8, column=0, columnspan=6, padx=5, sticky=NSEW)

        self.family_table = ttk.Treeview(self.firstSection, columns=('Connection', 'PIB', 'BirthDate'), show='headings',
                                         height=4)
        self.family_table.heading('Connection', text="Ступінь родинного зв'язку (склад сім'ї)")
        self.family_table.heading('PIB', text='ПІБ')
        self.family_table.heading('BirthDate', text='Рік народження')
        self.family_table.grid(row=17, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)

        # Entries
        self.lastName_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.lastName_Entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.firstName_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.firstName_Entry.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        self.patronymic_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.patronymic_Entry.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        self.birthDate_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.birthDate_Entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.nationality_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.nationality_Entry.grid(row=1, column=3, sticky=W, padx=5, pady=5)

        self.education_Entry = ttk.Entry(self.firstSection, justify='center')
        self.education_Entry.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)

        self.graduateSchool_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.graduateSchool_Entry.grid(row=7, column=1, sticky=W, padx=5, pady=5)
        self.adjunct_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.adjunct_Entry.grid(row=7, column=3, sticky=W, padx=5, pady=5)
        self.doctoralStudies_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.doctoralStudies_Entry.grid(row=7, column=5, sticky=W, padx=5, pady=5)

        self.lastWork_Entry = ttk.Entry(self.firstSection, width=30, justify='center')
        self.lastWork_Entry.grid(row=9, column=1, sticky=W, padx=5, pady=5)
        self.lastPost_Entry = ttk.Entry(self.firstSection, width=30, justify='center')
        self.lastPost_Entry.grid(row=9, column=3, sticky=W, padx=5, pady=5)

        self.workExpDate_Entry = ttk.Entry(self.firstSection, width=18, justify='center')
        self.workExpDate_Entry.grid(row=10, column=1, padx=5, pady=5, sticky=W)
        self.workExpDays_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpDays_Entry.grid(row=10, column=2, padx=5, pady=5, sticky=W)
        self.workExpMonths_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpMonths_Entry.grid(row=10, column=3, padx=5, pady=5, sticky=W)
        self.workExpYears_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpYears_Entry.grid(row=10, column=3, padx=5, pady=5, sticky=E)

        self.workBonusDays_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusDays_Entry.grid(row=11, column=2, padx=5, pady=5, sticky=W)
        self.workBonusMonths_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusMonths_Entry.grid(row=11, column=3, padx=5, pady=5, sticky=W)
        self.workBonusYears_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusYears_Entry.grid(row=11, column=3, padx=5, pady=5, sticky=E)

        self.workFireDate_Entry = ttk.Entry(self.firstSection, width=20, justify='center')
        self.workFireDate_Entry.grid(row=13, padx=5, pady=5, sticky=W)
        self.workFireReason_Entry = ttk.Entry(self.firstSection, width=100, justify='center')
        self.workFireReason_Entry.grid(row=13, column=1, columnspan=4, padx=5, pady=5, sticky=W)

        self.retire_Entry = ttk.Entry(self.firstSection, width=124, justify='center')
        self.retire_Entry.grid(row=15, columnspan=6, padx=5, pady=5, sticky=W)

        self.family_Entry = ttk.Entry(self.firstSection, justify='center')
        self.family_Entry.grid(row=16, column=1, columnspan=5, padx=5, pady=5, sticky=NSEW)

        self.residence_Entry = ttk.Entry(self.firstSection, justify='center')
        self.residence_Entry.grid(row=19, columnspan=6, padx=5, pady=5, sticky=NSEW)

        self.registeredResidence_Entry1 = ttk.Entry(self.firstSection, justify='center', width=95)
        self.registeredResidence_Entry1.grid(row=20, column=1, columnspan=5, padx=5, pady=5, sticky=E)
        self.registeredResidence_Entry2 = ttk.Entry(self.firstSection, justify='center', width=45)
        self.registeredResidence_Entry2.grid(row=21, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        self.passportSeries_Entry = ttk.Entry(self.firstSection, justify='center', width=11)
        self.passportSeries_Entry.grid(row=21, column=2, padx=5, pady=5, sticky=E)
        self.passportNumber_Entry = ttk.Entry(self.firstSection, justify='center', width=25)
        self.passportNumber_Entry.grid(row=21, column=3, padx=5, pady=5, sticky=E)
        self.passportIssuedBy_Entry = ttk.Entry(self.firstSection, justify='center')
        self.passportIssuedBy_Entry.grid(row=22, column=0, columnspan=4, padx=5, pady=5, sticky=NSEW)
        self.passportDate_Entry = ttk.Entry(self.firstSection, justify='center')
        self.passportDate_Entry.grid(row=22, column=5, padx=5, pady=5, sticky=W)

        # Buttons
        self.openDocsTab_Button = ttk.Button(self.mainScrolledFrame.interior, text="Відкрити вікно з документами",
                                             command=self.open_docs_tab)
        self.openDocsTab_Button.pack(fill=BOTH, padx=5, pady=5)
        self.closeTab_Button = ttk.Button(self.mainScrolledFrame.interior, text="Зберегти та закрити вкладку",
                                          command=self.close_tab)
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

        notebook.insert("end", self.mainFrame, text=name)

        self.get_info_from_db(self.id)

    def get_info_from_db(self, worker_id):
        info = db.get_worker_full_info(worker_id)
        self.lastName_Entry.insert(END, info[0][1])
        self.firstName_Entry.insert(END, info[0][2])
        self.patronymic_Entry.insert(END, info[0][3])
        self.birthDate_Entry.insert(END, info[0][5])

        img = Image.open(BytesIO(info[0][7]))
        self.photo = ImageTk.PhotoImage(img)
        self.photo_label.config(image=self.photo)

        self.nationality_Entry.insert(END, info[0][9])
        self.education_Entry.insert(END, info[0][10])

        self.education_table1.insert(parent='', index=0, values=(info[0][12], info[0][13], info[0][14]))
        self.education_table2.insert(parent='', index=0, values=(info[0][15], info[0][16], info[0][17]))

        if info[0][18] == 1:
            self.graduateSchool_Entry.insert(END, "X")
        elif info[0][18] == 2:
            self.adjunct_Entry.insert(END, "X")
        elif info[0][18] == 3:
            self.doctoralStudies_Entry.insert(END, "X")

        self.education_table3.insert(parent='', index=0, values=(info[0][19], info[0][20], info[0][21], info[0][22]))

    def close_tab(self):
        self.notebook.forget(self.mainFrame)

    def open_docs_tab(self):
        self.docsTab = DocumentsInfo(self.notebook, self.name)


class DocumentsInfo:
    def __init__(self, notebook, name):
        self.notebook = notebook

        self.mainFrame = ttk.Frame(notebook)

        notebook.insert("end", self.mainFrame, text=name + " док.")

        self.close_tab_Button = ttk.Button(self.mainFrame, text="Зберегти та закрити", command=self.close_tab)
        self.close_tab_Button.pack()

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
