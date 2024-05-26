import sqlite3
import datetime
import locale
import re


class HandleDataBaseModel:
    def __init__(self):
        self.connection = sqlite3.connect('HumanResourceDepartment.db')
        self.cursor = self.connection.cursor()
        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')

    @staticmethod
    def is_valid_date(date_string):
        date_pattern = r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$'
        if date_string:
            if re.fullmatch(date_pattern, date_string):
                return True
            else:
                return False
        else:
            return True

    def get_worker_info(self, worker_id):
        self.cursor.execute("SELECT * FROM Workers WHERE id = ?", (worker_id,))
        info = list(self.cursor.fetchone())[:-1]
        self.cursor.execute("SELECT * FROM Appointment WHERE worker_id = ? ORDER BY Date DESC",
                            (worker_id,))
        info.append(self.cursor.fetchall()[0][3])
        self.cursor.execute("SELECT Salary_in_one_worker FROM Posts WHERE Post_name = ?", (info[6],))
        info.append(self.cursor.fetchone()[0])
        info = tuple(info)
        return info

    def get_worker_full_info(self, worker_id):
        try:
            self.connection.execute("begin transaction")
            output = []

            self.cursor.execute("SELECT * FROM Workers JOIN FullInfo ON Workers.id = FullInfo.worker_id "
                                "WHERE Workers.id = ?", (worker_id,))

            info = self.cursor.fetchall()[0]
            temp = []
            for el in range(len(info)):
                if el != 0 and el != 6 and el != 7:
                    temp.append(info[el])
            output.append(temp)

            self.cursor.execute("SELECT * FROM Education WHERE Education.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall())

            self.cursor.execute("SELECT * FROM PostGraduationEducation "
                                "WHERE PostGraduationEducation.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall())

            self.cursor.execute("SELECT * FROM Family WHERE Family.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall())

            self.cursor.execute("SELECT * FROM Military WHERE Military.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall()[0][1:])

            self.cursor.execute("SELECT * FROM ProfessionalEducation "
                                "WHERE ProfessionalEducation.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall())

            self.cursor.execute("SELECT Appointment.ProfName, Posts.Salary_in_one_worker FROM "
                                "Appointment JOIN Posts on Appointment.ProfName = Posts.Post_name")
            salary = self.cursor.fetchall()
            for i in salary:
                self.cursor.execute("UPDATE Appointment set Salary = ? WHERE ProfName = ?",
                                    (i[1], i[0]))
            self.connection.commit()

            self.cursor.execute("SELECT * FROM Appointment WHERE Appointment.worker_id = ?",
                                (worker_id,))
            output.append(self.cursor.fetchall())

            self.cursor.execute("SELECT * FROM Vacation WHERE Vacation.worker_id = ?", (worker_id,))
            output.append(self.cursor.fetchall())

            return output
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def update_info(self, worker_id, info, mil_info):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute("select unit_name from Workers where id = ?", (worker_id,))
            unit_name = self.cursor.fetchone()
            if unit_name:
                unit_name = unit_name[0]
            self.cursor.execute("delete from Workers where id = ?", (worker_id,))
            self.cursor.execute("delete from FullInfo where worker_id = ?", (worker_id,))
            self.cursor.execute("delete from Military where worker_id = ?", (worker_id,))

            if self.is_valid_date(info[3]):
                self.cursor.execute("insert into Workers (id, LastName, FirstName, Patronymic, BirthDate)"
                                    "values (?, ?, ?, ?, ?)", tuple([worker_id] + info[0:4]))
            else:
                self.connection.rollback()
                return "err"
            self.cursor.execute("update Workers set Photo = ? where id= ?",
                                (sqlite3.Binary(info[4]), worker_id))
            self.cursor.execute("update Workers set unit_name = ? where id=?", (unit_name, worker_id))

            if (self.is_valid_date(info[9]) and
                    self.is_valid_date(info[16]) and
                    self.is_valid_date(info[26]) and
                    self.is_valid_date(info[29])):
                self.cursor.execute("insert into FullInfo (worker_id, Nationality, Education, LastWork, "
                                    "LastWorkPost, WorkExperienceDate, WorkExperienceDays, WorkExperienceMonths, "
                                    "WorkExperienceYears, WorkBonusDays, WorkBonusMonths, WorkBonusYears, OldFireDate, "
                                    "OldFireReason, Pension, FamilyStatus, ActualResidence, RegisteredResidence, "
                                    "RegisteredResidence_cont, PassportSeries, PassportNumber, PassportIssuedBy, "
                                    "PassportIssueDate, AdditionalInfo, AdditionalInfo_cont, FireDate, FireReason, "
                                    "PersonnelServiceEmployeePost, PersonnelServiceEmployeeSign, "
                                    "PersonnelServiceEmployeePIB, EmployeePIB, EmployeeSign, EmployeeFireDate, "
                                    "EmployeeFireYear) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                                    "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple([worker_id]+info[5:]))
            else:
                self.connection.rollback()
                return "err"

            self.cursor.execute("insert into Military (worker_id, AccountingGroup, Suitability, AccountingCategory, "
                                "CommitteeNameRegistration, AccountingCategory_cont, CommitteeNameRegistration_cont, "
                                "Compound, CommitteeNameLiving, Rank, CommitteeNameLiving_cont, Specialty, "
                                "SpecialAccounting)"
                                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple([worker_id] + mil_info))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def update_table(self, worker_id, tables_list, table_number, data):
        try:
            self.connection.execute("begin transaction")
            if tables_list == 0:
                if table_number == 0:
                    self.cursor.execute("DELETE FROM Education WHERE worker_id = ?", (worker_id,))
                    for row in data:
                        self.cursor.execute("INSERT INTO Education ("
                                            "worker_id, UniName, Diploma, GraduationYear, "
                                            "Specialty, Qualification, EducationForm)"
                                            "VALUES (?, ?, ?, ?, ?, ?, ?)", tuple([worker_id] + row))
                elif table_number == 2:
                    self.cursor.execute("DELETE FROM PostGraduationEducation WHERE worker_id = ?",
                                        (worker_id,))
                    for row in data:
                        self.cursor.execute("INSERT INTO PostGraduationEducation ("
                                            "worker_id, PostGradUniName, "
                                            "PostGradDiploma, PostGradGradYear, PostGradDegree)"
                                            "VALUES (?, ?, ?, ?, ?)", tuple([worker_id] + row))
                elif table_number == 3:
                    self.cursor.execute("DELETE FROM Family WHERE worker_id = ?", (worker_id,))
                    for row in data:
                        if self.is_valid_date(row[-1]):
                            self.cursor.execute("INSERT INTO Family (worker_id, member, PIB, BirthDate) VALUES "
                                                "(?, ?, ?, ?)", tuple([worker_id] + row))
                        else:
                            self.connection.rollback()
                            return "err"
            else:
                if table_number == 0:
                    self.cursor.execute("DELETE FROM ProfessionalEducation WHERE worker_id = ?",
                                        (worker_id,))
                    for row in data:
                        if self.is_valid_date(row[0]):
                            self.cursor.execute(
                                "INSERT INTO ProfessionalEducation(worker_id, Date, Name, Period, Type, Form, "
                                "Document) VALUES (?, ?, ?, ?, ?, ?, ?)", tuple([worker_id] + row))
                        else:
                            self.connection.rollback()
                            return "err"
                elif table_number == 1:
                    self.cursor.execute("DELETE FROM Appointment WHERE worker_id = ?", (worker_id,))
                    for row in data:
                        if self.is_valid_date(row[0]):
                            self.cursor.execute("INSERT INTO Appointment (worker_id, Date, Name, ProfName, Code, "
                                                "Salary, OrderBasis, Sign) "
                                                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", tuple([worker_id] + row))
                        else:
                            self.connection.rollback()
                            return "err"
                elif table_number == 2:
                    self.cursor.execute("DELETE FROM Vacation WHERE worker_id = ?", (worker_id,))
                    for row in data:
                        if self.is_valid_date(row[2]) and self.is_valid_date(row[3]):
                            self.cursor.execute("INSERT INTO Vacation(worker_id, Type, Period, Start, End, OrderBasis)"
                                                "VALUES (?, ?, ?, ?, ?, ?)", tuple([worker_id] + row))
                        else:
                            self.connection.rollback()
                            return "err"
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def create_new_worker(self):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute("select * from Workers order by id desc")
            output = self.cursor.fetchall()[0][0] + 1
            self.cursor.execute("insert into Workers(id, LastName, FirstName, Patronymic, BirthDate, Photo, unit_name)"
                                "values (?, ?, ?, ?, ?, ?, ?)", (output, '', '', '', '', None, None))
            self.connection.commit()
            return output
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def upload_image(self, worker_id, image_data):
        try:
            self.cursor.execute("update Workers set Photo = ? where id = ?",
                                (sqlite3.Binary(image_data), worker_id))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def delete_worker(self, worker_id):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute(f"select name from sqlite_master where type='table' and name!='WorkersProjects'")
            tables = self.cursor.fetchall()
            for x in tables:
                self.cursor.execute(f"pragma table_info({x[0]})")
                self.cursor.execute(f"delete from {x[0]} where {self.cursor.fetchall()[0][1]}={worker_id}")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_worker_projects(self, worker_id):
        self.cursor.execute("select id, Collaborators from WorkersProjects")
        c = self.cursor.fetchall()
        c = [(i[0], [self.get_worker_id(*e.split()) for e in [j.strip() for j in i[1].split(',')]]) for i in c]

        projects = []
        for i in c:
            if int(worker_id) in i[1]:
                self.cursor.execute("select * from WorkersProjects where id = ?", (i[0],))
                projects.append(self.cursor.fetchone())

        return projects

    def get_all_projects(self):
        self.cursor.execute(f"select * from WorkersProjects order by id")
        return self.cursor.fetchall()

    def get_worker_id(self, last_name, first_name):
        self.cursor.execute(f"select id from Workers where LastName=? and FirstName=?",
                            (last_name, first_name))
        return self.cursor.fetchone()[0]

    def update_projects_table(self, data):
        try:
            self.connection.execute("begin transaction")
            for row in data:
                self.cursor.execute("delete from WorkersProjects where id=?", (row[0],))
                self.cursor.execute('insert into WorkersProjects(id, name, cost, start, end, collaborators) '
                                    'VALUES (?, ?, ?, ?, ?, ?)', tuple(row))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def get_units(self):
        try:
            self.connection.execute("begin transaction")
            rows = []
            self.cursor.execute(f'select Name from Units')
            names = self.cursor.fetchall()
            for i in range(len(names)):
                row = [names[i][0]]

                self.cursor.execute("select id from Workers where unit_name = ?", (names[i][0],))
                try:
                    ids = [i[0] for i in self.cursor.fetchall()]
                except TypeError:
                    ids = []

                self.cursor.execute("select count(*) from Workers where unit_name = ?", (names[i][0],))
                row.append(self.cursor.fetchone()[0])

                k = 0
                cost = 0
                self.cursor.execute("select projects_id from Units where name = ?", (names[i][0],))
                projects = self.cursor.fetchone()[0]

                if projects:
                    for p in projects.split(','):
                        self.cursor.execute('select End from WorkersProjects where id = ?', (p,))
                        end_date = datetime.datetime.strptime(self.cursor.fetchone()[0], "%d-%m-%Y").date()
                        current_date = datetime.date.today().strftime("%Y-%m-%d")
                        formatted_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
                        if end_date > formatted_date:
                            k += 1

                        self.cursor.execute('select Cost from WorkersProjects where id = ?', (p,))
                        cost += self.cursor.fetchone()[0]

                row.append(k)
                row.append(len(projects.split(',')) if projects else 0)
                row.append(cost)
                row.append(projects if projects else None)
                rows.append((ids, row))

            self.cursor.execute(f"delete from Units")
            for row in rows:
                self.cursor.execute(f'insert into Units(Name, WorkersQuantity, UnfinishedProjectsQuantity, '
                                    f'AllProjectsQuantity, TotalCost, projects_id) values (?, ?, ?, ?, ?, ?)',
                                    tuple(row[1]))
            self.connection.commit()
            return rows
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_unit_workers(self, unit_name):
        self.cursor.execute("select id from Workers where unit_name = ?", (unit_name,))
        return [i[0] for i in self.cursor.fetchall()]

    def get_unit_projects(self, unit_name):
        try:
            self.cursor.execute("select projects_id from Units where Name = ?", (unit_name,))
            projects = self.cursor.fetchone()[0].split(',')
            output = []
            for project in projects:
                self.cursor.execute("select id, Name, Cost, Start, End, Collaborators from WorkersProjects "
                                    "where id = ?", (project,))
                output.append(self.cursor.fetchone())
            return output
        except TypeError:
            pass
        except AttributeError:
            pass

    def get_not_unit_workers(self, unit_name):
        self.cursor.execute("select id, LastName, FirstName, Patronymic from Workers "
                            "where unit_name != ? or unit_name is null", (unit_name,))

        not_unit_workers = self.cursor.fetchall()
        workers = []
        for i in not_unit_workers:
            self.cursor.execute("select unit_name from Workers where id = ?", (i[0],))
            worker = list(i)
            try:
                unit = self.cursor.fetchone()[0]
                worker.append(f'знаходиться у підрозділі: {unit}' if unit is not None
                              else 'не знаходиться у підрозділах')
            except TypeError:
                worker.append('не знаходиться у підрозділах')
            workers.append(worker)
        return workers

    def set_worker_unit(self, worker_id, unit_name):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute("update Workers set unit_name = ? where id = ?", (unit_name, worker_id))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def update_units(self, old_units, units, ids):
        try:
            self.connection.execute("begin transaction")

            self.cursor.execute("select projects_id from Units")
            projects = [i[0] for i in self.cursor.fetchall()]
            if len(projects) < int(ids[-1][1:], 16):
                for i in range(int(ids[-1][1:], 16)-len(projects)):
                    projects.append(None)

            indexes = [int(i[1:])-1 for i in ids]

            projects = [projects[i] for i in indexes]

            excluded_elements = [old_units[i] for i in range(len(old_units))
                                 if i not in indexes and old_units[i] != ([], None)]

            self.cursor.execute("delete from Units")

            for i in zip([old_units[j] for j in indexes], units, projects):
                self.cursor.execute(f"insert into Units values (?, ?, ?, ?, ?, ?)",
                                    (i[1][1], None, None, None, None, i[2]))

                for j in i[1][0]:
                    self.cursor.execute("update Workers set unit_name = ? where id = ?", (i[1][1], j))

                for j in excluded_elements:
                    for e in j[0]:
                        self.cursor.execute("update Workers set unit_name = null where id=?", (e,))

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def get_id_of_workers(self):
        self.cursor.execute("select id from Workers")
        return [i[0] for i in self.cursor.fetchall()]

    def get_posts(self):
        try:
            self.connection.execute("begin transaction")
            rows = []
            self.cursor.execute('select Post_name from Posts')
            names = self.cursor.fetchall()
            for i in range(len(names)):
                row = [names[i][0]]
                help_count = int()
                self.cursor.execute("select Salary_in_one_worker from Posts where Post_name = ?",
                                    (names[i][0],))
                help_salary = self.cursor.fetchone()[0]
                row.append(help_salary)

                self.cursor.execute("select Work_time from Posts where Post_name = ?", (names[i][0],))
                row.append(self.cursor.fetchone()[0])

                self.cursor.execute("select id from Workers")
                workers_id = [j[0] for j in self.cursor.fetchall()]
                for j in workers_id:
                    self.cursor.execute("select Date, ProfName from Appointment where worker_id = ?", (j,))
                    date_prof = self.cursor.fetchall()
                    sorted_help = sorted(date_prof, key=lambda x: x[0])
                    if sorted_help[-1][1] == names[i][0]:
                        help_count += 1
                row.append(help_count)

                row.append(help_count * help_salary)

                rows.append(row)

            for row in rows:
                self.cursor.execute("delete from Posts where Post_name = ?", (row[0],))
                self.cursor.execute(f'insert into Posts(Post_name, Salary_in_one_worker, Work_time, '
                                    f'Sum_of_workers, Sum_salary) values (?, ?, ?, ?, ?)', tuple(row))
            self.connection.commit()
            return rows
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def write_post(self, tables_elements):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute("delete from Posts")
            for i in tables_elements:
                self.cursor.execute('insert into Posts(Post_name, Salary_in_one_worker, Work_time) '
                                    'values (?, ?, ?)', tuple(i))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def get_projects_for_unit(self):
        self.cursor.execute("select Name from WorkersProjects")
        return [i[0] for i in self.cursor.fetchall()]

    def get_project_data_by_name(self, name):
        self.cursor.execute("select * from WorkersProjects where Name = ?", (name,))
        return self.cursor.fetchone()

    def set_unit_projects(self, projects, unit_name):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute("update Units set projects_id=? where Name=?", (projects, unit_name))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def get_work_hours(self, post_name):
        rows = []
        help1 = []
        help2 = []
        now = datetime.datetime.now()

        self.cursor.execute("select id from Workers")
        workers_id = [j[0] for j in self.cursor.fetchall()]
        for j in workers_id:
            self.cursor.execute("select worker_id, Date, ProfName from Appointment where worker_id = ?", (j,))
            id_date_prof = self.cursor.fetchall()
            sorted_help = sorted(id_date_prof, key=lambda x: x[1])
            if sorted_help[-1][2] == post_name:
                rows.append(sorted_help[-1])
        for i in range(len(rows)):
            for j in range(3):
                help1.append(rows[i][j])
            help2.append(help1)
            help1 = []
            help2[i][1] = (now.date() - datetime.datetime.strptime(rows[i][1], "%d-%m-%Y").date()).days

        return help2

    def get_projects_cost(self):
        projects_cost = {}

        self.cursor.execute("select LastName, FirstName from Workers")
        workers = [" ".join(j) for j in self.cursor.fetchall()]

        for i in workers:
            projects_cost[i] = 0

        self.cursor.execute("select Cost, Collaborators from WorkersProjects")
        collaborators = self.cursor.fetchall()

        for i in collaborators:
            for j in i[1].split(", "):
                try:
                    projects_cost[j] += i[0]
                except KeyError:
                    pass

        return projects_cost

    def get_all_worker(self):
        self.cursor.execute("select id, Lastname, FirstName from Workers")
        return [(j[0], " ".join(j[1:])) for j in self.cursor.fetchall()]
