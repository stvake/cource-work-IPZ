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
        for i in range(db.get_workers_quantity()):
            Worker(i+1, self.frame.interior, self.notebook)

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
    def __init__(self, worker_id, parent, notebook):
        super().__init__(parent)

        self.notebook = notebook

        self.id = worker_id

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

        self.get_info()

    def get_info(self):
        for x in db.get_worker_info(self.id):
            self.name_text.config(state=NORMAL)
            self.email_text.config(state=NORMAL)
            self.birth_date_text.config(state=NORMAL)
            self.post_text.config(state=NORMAL)

            self.name_text.insert(1.0, f"{x[1]} {x[2]} {x[3]}")
            self.email_text.insert(1.0, f"{x[4]}")
            self.birth_date_text.insert(1.0, f"{x[5]}")
            self.post_text.insert(1.0, f"{x[6]}")

            img = Image.open(BytesIO(x[7]))
            self.photo = ImageTk.PhotoImage(img)
            self.photo_label.config(image=self.photo)

            self.name_text.config(state=DISABLED)
            self.email_text.config(state=DISABLED)
            self.birth_date_text.config(state=DISABLED)
            self.post_text.config(state=DISABLED)

    def more_info(self):
        self.info_page = FullWorkerInfo(self.notebook, self)

    def delete(self):
        # db.delete_worker(self.id)
        # self.destroy()
        pass


class FullWorkerInfo:
    def __init__(self, notebook, worker):
        self.worker = worker

        self.id = worker.id

        self.name = worker.name_text.get(1.0, END)[:-1]

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
        self.firstSection = LabelFrame(self.mainScrolledFrame.interior, text="І. ЗАГАЛЬНІ ВІДОМОСТІ")
        self.firstSection.pack(fill=BOTH, padx=5, pady=5)
        self.secondSection = LabelFrame(self.mainScrolledFrame.interior, text="ІІ. ВІДОМОСТІ ПРО ВІЙСЬКОВИЙ ОБЛІК")
        self.secondSection.pack(fill=BOTH, padx=5, pady=5)
        self.thirdSection = LabelFrame(self.mainScrolledFrame.interior,
                                       text="ІІІ. ПРОФЕСІЙНА ОСВІТА НА ВИРОБНИЦТВІ "
                                            "(ЗА РАХУНОК ""ПІДПРИЄМСТВА - РОБОТОДАВЦЯ)")
        self.thirdSection.pack(fill=BOTH, padx=5, pady=5)
        self.fourthSection = LabelFrame(self.mainScrolledFrame.interior, text="IV. ПРИЗНАЧЕННЯ І ПЕРЕВЕДЕННЯ")
        self.fourthSection.pack(fill=BOTH, padx=5, pady=5)
        self.fifthSection = LabelFrame(self.mainScrolledFrame.interior, text="V. ВІДПУСТКИ")
        self.fifthSection.pack(fill=BOTH, padx=5, pady=5)
        self.sixthSection = Frame(self.mainScrolledFrame.interior)
        self.sixthSection.pack(fill=BOTH, padx=5, pady=5)

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

        self.pension_Label = ttk.Label(self.firstSection, text="Відомості про отримання пенсії (у разі наявності "
                                                               "вказати вид пенсійних виплат згідно з чинним "
                                                               "законодавством)")
        self.pension_Label.grid(row=14, columnspan=6, padx=5, pady=5, sticky=W)

        self.family_Label = ttk.Label(self.firstSection, text="Родинний стан")
        self.family_Label.grid(row=16, column=0, padx=5, pady=5, sticky=W)

        self.actualResidence_Label = ttk.Label(self.firstSection, text="Місце фактичного проживання (область, місто, "
                                                                       "район, вулиця, № будинку, квартири, номер "
                                                                       "контактного телефону, поштовий індекс)")
        self.actualResidence_Label.grid(row=18, columnspan=6, padx=5, pady=5, sticky=W)

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
        self.passportIssueDate_Label = ttk.Label(self.firstSection, text="дата видачі")
        self.passportIssueDate_Label.grid(row=22, column=4, padx=5, pady=5)

        self.militaryRecordGroup_Label = ttk.Label(self.secondSection, text="Група обліку")
        self.militaryRecordGroup_Label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.militaryRecordSuitability_Label = ttk.Label(self.secondSection, text="Придатність до військової служби")
        self.militaryRecordSuitability_Label.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.militaryRecordCategories_Label = ttk.Label(self.secondSection, text="Категорія обліку")
        self.militaryRecordCategories_Label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.militaryRecordNameReg_Label = ttk.Label(self.secondSection,
                                                     text="Назва райвіськомату за місцем реєстрації")
        self.militaryRecordNameReg_Label.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.militaryRecordCompound_Label = ttk.Label(self.secondSection, text="Склад")
        self.militaryRecordCompound_Label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.militaryRecordNameLiving_Label = ttk.Label(self.secondSection,
                                                        text="Назва райвіськомату за місцем фактичного проживання")
        self.militaryRecordNameLiving_Label.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        self.militaryRecordRank_Label = ttk.Label(self.secondSection, text="Військове звання")
        self.militaryRecordRank_Label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.militaryRecordSpecialty_Label = ttk.Label(self.secondSection, text="Військово-облікова спеціальність №")
        self.militaryRecordSpecialty_Label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        self.militaryRecordSpecial_Label = ttk.Label(self.secondSection, text="Перебування на спеціальному обліку")
        self.militaryRecordSpecial_Label.grid(row=5, column=2, padx=5, pady=5, sticky=W)

        self.appointment_Label = ttk.Label(self.fourthSection, text="* Відповідно до Класифікатора професій "
                                                                    "ДК 003-2005, затвердженого наказом Держстандарту "
                                                                    "України від 26.12.2005 N 375,\n з урахуванням "
                                                                    "позначки кваліфікаційного рівня "
                                                                    "(6 знаків, наприклад, код професії 'муляр'"
                                                                    "- 7122.2).")
        self.appointment_Label.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky=W)

        self.additionalInfo_Label = ttk.Label(self.sixthSection, text="Додаткові відомості")
        self.additionalInfo_Label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.dismissalInfo_Label = ttk.Label(self.sixthSection, text="Дата і причина звільнення (підстава)")
        self.dismissalInfo_Label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.personnelServiceEmployee_Label = ttk.Label(self.sixthSection, text="Працівник кадрової служби")
        self.personnelServiceEmployee_Label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.position_Label = ttk.Label(self.sixthSection, text="(посада)")
        self.position_Label.grid(row=4, column=1, padx=5, pady=(0, 5))
        self.Sign_Label = ttk.Label(self.sixthSection, text="(підпис)")
        self.Sign_Label.grid(row=4, column=2, padx=5, pady=(0, 5))
        self.PIB_Label = ttk.Label(self.sixthSection, text="(П. І. Б)")
        self.PIB_Label.grid(row=4, column=3, columnspan=3, padx=5, pady=(0, 5))

        self.workerName_Label = ttk.Label(self.sixthSection, text="Підпис працівника")
        self.workerName_Label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
        self.quotationMarks1_Label = ttk.Label(self.sixthSection, text='"')
        self.quotationMarks1_Label.grid(row=5, column=2, padx=5, pady=5, sticky=W)
        self.quotationMarks2_Label = ttk.Label(self.sixthSection, text='"')
        self.quotationMarks2_Label.grid(row=5, column=2, padx=5, pady=5, sticky=E)
        self.twenty_Label = ttk.Label(self.sixthSection, text="20")
        self.twenty_Label.grid(row=5, column=4, padx=(5, 0), pady=5, sticky=W)
        self.workerYear_Label = ttk.Label(self.sixthSection, text="року")
        self.workerYear_Label.grid(row=5, column=4, padx=5, pady=5, sticky=E)
        self.Date_Label = ttk.Label(self.sixthSection, text="(дата)")
        self.Date_Label.grid(row=6, column=3, padx=5, pady=(0, 5))

        # Treeviews
        self.tables_firstSection = []
        self.tables_other = []

        self.education_table1 = ttk.Treeview(self.firstSection, columns=('Name', 'Diploma', 'year'), show='headings',
                                             height=4)
        self.education_table1.heading('Name', text='Назва освітнього закладу')
        self.education_table1.heading('Diploma', text='Диплом (свідоцтво), серія, номер')
        self.education_table1.heading('year', text='Рік закінчення')
        self.education_table1.grid(row=4, column=0, columnspan=6, padx=5, sticky=NSEW)
        self.tables_firstSection.append(self.education_table1)

        self.education_table2 = ttk.Treeview(self.firstSection, columns=('Spec', 'Cual', 'Form'), show='headings',
                                             height=4)
        self.education_table2.heading('Spec', text='Спеціальність (професія) за дипломом (свідоцтвом)')
        self.education_table2.heading('Cual', text='Кваліфікація за дипломом (свідоцтвом)')
        self.education_table2.heading('Form', text='Форма навчання')
        self.education_table2.grid(row=5, column=0, columnspan=6, padx=5, sticky=NSEW)
        self.tables_firstSection.append(self.education_table2)

        self.education_table3 = ttk.Treeview(self.firstSection, columns=('Name', 'Diploma', 'year', 'degree'),
                                             show='headings', height=4)
        self.education_table3.heading('Name', text='Назва освітнього, наукового  закладу')
        self.education_table3.heading('Diploma', text='Диплом, номер, дата видачі')
        self.education_table3.heading('year', text='Рік закінчення')
        self.education_table3.heading('degree', text='Науковий ступінь, учене звання')
        self.education_table3.grid(row=8, column=0, columnspan=6, padx=5, sticky=NSEW)
        self.tables_firstSection.append(self.education_table3)

        self.family_table = ttk.Treeview(self.firstSection, columns=('Connection', 'PIB', 'BirthDate'), show='headings',
                                         height=4)
        self.family_table.heading('Connection', text="Ступінь родинного зв'язку (склад сім'ї)")
        self.family_table.heading('PIB', text='ПІБ')
        self.family_table.heading('BirthDate', text='Рік народження')
        self.family_table.grid(row=17, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        self.tables_firstSection.append(self.family_table)

        self.professionalEducation_table = ttk.Treeview(self.thirdSection,
                                                        columns=('Date', 'Name', 'Period', 'Type', 'Form',
                                                                 'Document'), show='headings', height=4)
        self.professionalEducation_table.heading('Date', text='Дата')
        self.professionalEducation_table.heading('Name', text='Назва структурного підрозділу')
        self.professionalEducation_table.heading('Period', text='Період навчання')
        self.professionalEducation_table.heading('Type', text='Вид навчання')
        self.professionalEducation_table.heading('Form', text='Форма навчання')
        self.professionalEducation_table.heading('Document', text='Назва документу, що посвідчує професійну освіту, '
                                                                  'ким виданий')

        self.professionalEducation_table.column('Date', width=147)
        self.professionalEducation_table.column('Name', width=147)
        self.professionalEducation_table.column('Period', width=147)
        self.professionalEducation_table.column('Type', width=147)
        self.professionalEducation_table.column('Form', width=147)
        self.professionalEducation_table.column('Document', width=147)
        self.professionalEducation_table.grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        self.tables_other.append(self.professionalEducation_table)

        self.appointment_table = ttk.Treeview(self.fourthSection, columns=('Date', 'Name', 'ProfName', 'Code', 'Salary',
                                                                           'Order', 'Sign'), show='headings', height=4)
        self.appointment_table.heading('Date', text='Дата')
        self.appointment_table.heading('Name', text='Назва структурного підрозділу (код)')
        self.appointment_table.heading('ProfName', text='Назва професії, посади')
        self.appointment_table.heading('Code', text='Код за КП*')
        self.appointment_table.heading('Salary', text='Розряд (оклад)')
        self.appointment_table.heading('Order', text='Підстава, наказ №')
        self.appointment_table.heading('Sign', text='Підпис працівника')

        self.appointment_table.column('Date', width=126)
        self.appointment_table.column('Name', width=126)
        self.appointment_table.column('ProfName', width=126)
        self.appointment_table.column('Code', width=126)
        self.appointment_table.column('Salary', width=126)
        self.appointment_table.column('Order', width=126)
        self.appointment_table.column('Sign', width=126)
        self.appointment_table.grid(row=0, column=0, columnspan=6, padx=5)
        self.tables_other.append(self.appointment_table)

        self.vacation_table = ttk.Treeview(self.fifthSection, columns=('Type', 'Period', 'Start', 'End', 'Order'),
                                           show='headings', height=4)
        self.vacation_table.heading('Type', text='Вид відпустки ')
        self.vacation_table.heading('Period', text='За який період')
        self.vacation_table.heading('Start', text='початку відпустки')
        self.vacation_table.heading('End', text='закінчення відпустки')
        self.vacation_table.heading('Order', text='Підстава, наказ №')

        self.vacation_table.column('Type', width=177)
        self.vacation_table.column('Period', width=177)
        self.vacation_table.column('Start', width=177)
        self.vacation_table.column('End', width=177)
        self.vacation_table.column('Order', width=177)
        self.vacation_table.grid(row=0, column=0, columnspan=6, padx=5, pady=5)
        self.tables_other.append(self.vacation_table)

        # Entries
        self.entries_general = []
        self.entries_secondSection = []

        self.lastName_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.lastName_Entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.lastName_Entry)
        self.firstName_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.firstName_Entry.grid(row=0, column=3, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.firstName_Entry)
        self.patronymic_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.patronymic_Entry.grid(row=0, column=5, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.patronymic_Entry)
        self.birthDate_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.birthDate_Entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.birthDate_Entry)
        self.nationality_Entry = ttk.Entry(self.firstSection, width=15, justify='center')
        self.nationality_Entry.grid(row=1, column=3, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.nationality_Entry)

        self.education_Entry = ttk.Entry(self.firstSection, justify='center')
        self.education_Entry.grid(row=3, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.education_Entry)

        self.graduateSchool_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.graduateSchool_Entry.grid(row=7, column=1, sticky=W, padx=5, pady=5)
        self.adjunct_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.adjunct_Entry.grid(row=7, column=3, sticky=W, padx=5, pady=5)
        self.doctoralStudies_Entry = ttk.Entry(self.firstSection, width=3, justify='center')
        self.doctoralStudies_Entry.grid(row=7, column=5, sticky=W, padx=5, pady=5)

        self.lastWork_Entry = ttk.Entry(self.firstSection, width=30, justify='center')
        self.lastWork_Entry.grid(row=9, column=1, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.lastWork_Entry)
        self.lastPost_Entry = ttk.Entry(self.firstSection, width=30, justify='center')
        self.lastPost_Entry.grid(row=9, column=3, sticky=W, padx=5, pady=5)
        self.entries_general.append(self.lastPost_Entry)

        self.workExpDate_Entry = ttk.Entry(self.firstSection, width=18, justify='center')
        self.workExpDate_Entry.grid(row=10, column=1, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workExpDate_Entry)
        self.workExpDays_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpDays_Entry.grid(row=10, column=2, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workExpDays_Entry)
        self.workExpMonths_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpMonths_Entry.grid(row=10, column=3, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workExpMonths_Entry)
        self.workExpYears_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workExpYears_Entry.grid(row=10, column=3, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.workExpYears_Entry)

        self.workBonusDays_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusDays_Entry.grid(row=11, column=2, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workBonusDays_Entry)
        self.workBonusMonths_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusMonths_Entry.grid(row=11, column=3, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workBonusMonths_Entry)
        self.workBonusYears_Entry = ttk.Entry(self.firstSection, width=10, justify='center')
        self.workBonusYears_Entry.grid(row=11, column=3, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.workBonusYears_Entry)

        self.workFireDate_Entry = ttk.Entry(self.firstSection, width=20, justify='center')
        self.workFireDate_Entry.grid(row=13, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workFireDate_Entry)
        self.workFireReason_Entry = ttk.Entry(self.firstSection, width=100, justify='center')
        self.workFireReason_Entry.grid(row=13, column=1, columnspan=4, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.workFireReason_Entry)

        self.pension_Entry = ttk.Entry(self.firstSection, width=124, justify='center')
        self.pension_Entry.grid(row=15, columnspan=6, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.pension_Entry)

        self.family_Entry = ttk.Entry(self.firstSection, justify='center')
        self.family_Entry.grid(row=16, column=1, columnspan=5, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.family_Entry)

        self.actualResidence_Entry = ttk.Entry(self.firstSection, justify='center')
        self.actualResidence_Entry.grid(row=19, columnspan=6, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.actualResidence_Entry)

        self.registeredResidence_Entry1 = ttk.Entry(self.firstSection, justify='center', width=95)
        self.registeredResidence_Entry1.grid(row=20, column=1, columnspan=5, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.registeredResidence_Entry1)
        self.registeredResidence_Entry2 = ttk.Entry(self.firstSection, justify='center', width=45)
        self.registeredResidence_Entry2.grid(row=21, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.registeredResidence_Entry2)
        self.passportSeries_Entry = ttk.Entry(self.firstSection, justify='center', width=11)
        self.passportSeries_Entry.grid(row=21, column=2, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.passportSeries_Entry)
        self.passportNumber_Entry = ttk.Entry(self.firstSection, justify='center', width=25)
        self.passportNumber_Entry.grid(row=21, column=3, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.passportNumber_Entry)
        self.passportIssuedBy_Entry = ttk.Entry(self.firstSection, justify='center')
        self.passportIssuedBy_Entry.grid(row=22, column=0, columnspan=4, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.passportIssuedBy_Entry)
        self.passportIssueDate_Entry = ttk.Entry(self.firstSection, justify='center')
        self.passportIssueDate_Entry.grid(row=22, column=5, padx=5, pady=5, sticky=W)
        self.entries_general.append(self.passportIssueDate_Entry)

        self.militaryRecordGroup_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordGroup_Entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordGroup_Entry)
        self.militaryRecordSuitability_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordSuitability_Entry.grid(row=0, column=3, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordSuitability_Entry)

        self.militaryRecordCategories_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordCategories_Entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordCategories_Entry)
        self.militaryRecordNameReg_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordNameReg_Entry.grid(row=1, column=3, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordNameReg_Entry)

        self.militaryRecordCategories2_Entry = ttk.Entry(self.secondSection, justify='center', width=56)
        self.militaryRecordCategories2_Entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordCategories2_Entry)
        self.militaryRecordNameReg2_Entry = ttk.Entry(self.secondSection, justify='center', width=75)
        self.militaryRecordNameReg2_Entry.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordNameReg2_Entry)

        self.militaryRecordCompound_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordCompound_Entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordCompound_Entry)
        self.militaryRecordNameLiving_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordNameLiving_Entry.grid(row=3, column=3, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordNameLiving_Entry)

        self.militaryRecordRank_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordRank_Entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordRank_Entry)
        self.militaryRecordNameLiving2_Entry = ttk.Entry(self.secondSection, justify='center', width=75)
        self.militaryRecordNameLiving2_Entry.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordNameLiving2_Entry)

        self.militaryRecordSpecialty_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordSpecialty_Entry.grid(row=5, column=1, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordSpecialty_Entry)
        self.militaryRecordSpecial_Entry = ttk.Entry(self.secondSection, justify='center')
        self.militaryRecordSpecial_Entry.grid(row=5, column=3, padx=5, pady=5, sticky=W)
        self.entries_secondSection.append(self.militaryRecordSpecial_Entry)

        self.additionalInfo_Entry1 = ttk.Entry(self.sixthSection, justify='center', width=120)
        self.additionalInfo_Entry1.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.additionalInfo_Entry1)
        self.additionalInfo_Entry2 = ttk.Entry(self.sixthSection, justify='center')
        self.additionalInfo_Entry2.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.additionalInfo_Entry2)

        self.dismissalDate_Entry = ttk.Entry(self.sixthSection, justify='center')
        self.dismissalDate_Entry.grid(row=2, column=1, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.dismissalDate_Entry)
        self.dismissalReason_Entry = ttk.Entry(self.sixthSection, justify='center')
        self.dismissalReason_Entry.grid(row=2, column=2, columnspan=4, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.dismissalReason_Entry)

        self.position_Entry = ttk.Entry(self.sixthSection, justify='center')
        self.position_Entry.grid(row=3, column=1, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.position_Entry)
        self.Sign_Entry = ttk.Entry(self.sixthSection, justify='center')
        self.Sign_Entry.grid(row=3, column=2, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.Sign_Entry)
        self.PIB_Entry = ttk.Entry(self.sixthSection, justify='center', width=60)
        self.PIB_Entry.grid(row=3, column=3, columnspan=3, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.PIB_Entry)

        self.workerName_Entry = ttk.Entry(self.sixthSection, justify="center", width=35)
        self.workerName_Entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=E)
        self.entries_general.append(self.workerName_Entry)
        self.workerSign_Entry = ttk.Entry(self.sixthSection, justify="center", width=18)
        self.workerSign_Entry.grid(row=5, column=2, padx=5, pady=5)
        self.entries_general.append(self.workerSign_Entry)
        self.workerDate_Entry = ttk.Entry(self.sixthSection, justify="center")
        self.workerDate_Entry.grid(row=5, column=3, padx=5, pady=5, sticky=NSEW)
        self.entries_general.append(self.workerDate_Entry)
        self.workerYear_Entry = ttk.Entry(self.sixthSection, justify="center", width=8)
        self.workerYear_Entry.grid(row=5, column=4, padx=(0, 5), pady=5)
        self.entries_general.append(self.workerYear_Entry)

        # Buttons
        self.openDocsTab_Button = ttk.Button(self.mainScrolledFrame.interior, text="Відкрити вікно з документами",
                                             command=self.open_docs_tab)
        self.openDocsTab_Button.pack(fill=BOTH, padx=5, pady=5)
        self.closeTab_Button = ttk.Button(self.mainScrolledFrame.interior, text="Зберегти та закрити вкладку",
                                          command=self.close_tab)
        self.closeTab_Button.pack(fill=BOTH, padx=5, pady=5)

        notebook.insert("end", self.mainFrame, text=self.name)

        self.get_info_from_db(self.id)

    def get_info_from_db(self, worker_id):
        info = db.get_worker_full_info(worker_id)

        for i in range(len(info[0])):
            if i < 4:
                if info[0][i] is not None:
                    self.entries_general[i].insert(END, info[0][i])
            elif i == 4:
                img = Image.open(BytesIO(info[0][i]))
                self.photo = ImageTk.PhotoImage(img)
                self.photo_label.config(image=self.photo)
            elif i > 4:
                if info[0][i] is not None:
                    self.entries_general[i - 1].insert(END, info[0][i])

        for row in info[1]:
            self.tables_firstSection[0].insert(parent='', index=END, values=row[1:])

        for row in info[1]:
            self.tables_firstSection[1].insert(parent='', index=END, values=row[4:])

        for row in info[2]:
            if row[1] == 1:
                self.graduateSchool_Entry.insert(END, "X")
            elif row[1] == 2:
                self.adjunct_Entry.insert(END, "X")
            elif row[1] == 3:
                self.doctoralStudies_Entry.insert(END, "X")
            self.tables_firstSection[2].insert(parent='', index=END, values=row[2:])

        for row in info[3]:
            self.tables_firstSection[3].insert(parent='', index=END, values=row[1:])

        for i in range(len(info[4])):
            if info[4][i] is not None:
                self.entries_secondSection[i].insert(END, info[4][i])

        for i in range(len(self.tables_other)):
            for row in info[5 + i]:
                self.tables_other[i].insert(parent='', index=END, values=row[1:])

    def close_tab(self):
        info = [i.get() for i in self.entries_general]
        db.update_info(self.id, info)

        self.worker.name_text.config(state=NORMAL)
        self.worker.email_text.config(state=NORMAL)
        self.worker.birth_date_text.config(state=NORMAL)
        self.worker.post_text.config(state=NORMAL)

        self.worker.name_text.delete(1.0, END)
        self.worker.birth_date_text.delete(1.0, END)

        self.worker.name_text.insert(END, info[0])
        self.worker.birth_date_text.insert(END, info[3])

        self.worker.name_text.config(state=DISABLED)
        self.worker.email_text.config(state=DISABLED)
        self.worker.birth_date_text.config(state=DISABLED)
        self.worker.post_text.config(state=DISABLED)

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
