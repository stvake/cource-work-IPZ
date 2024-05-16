import sqlite3
import datetime
import locale


class HandleDataBaseModel:
    def __init__(self):
        self.connection = sqlite3.connect('HumanResourceDepartment.db')
        self.cursor = self.connection.cursor()
        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')

    def get_worker_info(self, worker_id):
        self.cursor.execute(f"SELECT * FROM Workers WHERE id = {worker_id}")
        info = list(self.cursor.fetchone())[:-1]
        self.cursor.execute(f"SELECT * FROM Appointment WHERE worker_id = {worker_id} ORDER BY Date DESC")
        info.append(self.cursor.fetchall()[0][3])
        info = tuple(info)
        return info

    def get_worker_full_info(self, worker_id):
        output = []

        self.cursor.execute(f""" SELECT * FROM Workers JOIN FullInfo ON
        Workers.id = FullInfo.worker_id WHERE Workers.id = {worker_id}""")

        info = self.cursor.fetchall()[0]
        temp = []
        for el in range(len(info)):
            if el != 0 and el != 6 and el != 7:
                temp.append(info[el])
        output.append(temp)

        self.cursor.execute(f"""SELECT * FROM Education WHERE Education.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        self.cursor.execute(
            f"""SELECT * FROM PostGraduationEducation WHERE PostGraduationEducation.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        self.cursor.execute(f"""SELECT * FROM Family WHERE Family.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        self.cursor.execute(f"""SELECT * FROM Military WHERE Military.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall()[0][1:])

        self.cursor.execute(f"""SELECT * FROM ProfessionalEducation 
                                WHERE ProfessionalEducation.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        self.cursor.execute(f"""SELECT * FROM Appointment WHERE Appointment.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        self.cursor.execute(f"""SELECT * FROM Vacation WHERE Vacation.worker_id = {worker_id}""")
        output.append(self.cursor.fetchall())

        return output

    def update_info(self, worker_id, info, mil_info):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute(f"select unit_name from Workers where id = {worker_id}")
            unit_name = self.cursor.fetchone()[0]
            self.cursor.execute(f"delete from Workers where id = {worker_id}")
            self.cursor.execute(f"delete from FullInfo where worker_id = {worker_id}")
            self.cursor.execute(f"delete from Military where worker_id = {worker_id}")

            self.cursor.execute(f"insert into Workers (id, LastName, FirstName, Patronymic, BirthDate)"
                                f"values {tuple([worker_id] + info[0:4])}")
            self.cursor.execute(f"update Workers set Photo = ? where id={worker_id}",
                                (sqlite3.Binary(info[4]),))
            self.cursor.execute(f"update Workers set unit_name = '{unit_name}' where id={worker_id}")
            self.cursor.execute(f"insert into FullInfo (worker_id, Nationality, Education, LastWork, LastWorkPost, "
                                f"WorkExperienceDate, WorkExperienceDays, WorkExperienceMonths, WorkExperienceYears, "
                                f"WorkBonusDays, WorkBonusMonths, WorkBonusYears, OldFireDate, OldFireReason, Pension, "
                                f"FamilyStatus, ActualResidence, RegisteredResidence, RegisteredResidence_cont, "
                                f"PassportSeries, PassportNumber, PassportIssuedBy, PassportIssueDate, AdditionalInfo, "
                                f"AdditionalInfo_cont, FireDate, FireReason, PersonnelServiceEmployeePost, "
                                f"PersonnelServiceEmployeeSign, PersonnelServiceEmployeePIB, EmployeePIB, EmployeeSign,"
                                f"EmployeeFireDate, EmployeeFireYear)"
                                f"values {tuple([worker_id]+info[5:])}")
            self.cursor.execute(f"insert into Military (worker_id, AccountingGroup, Suitability, AccountingCategory, "
                                f"CommitteeNameRegistration, AccountingCategory_cont, CommitteeNameRegistration_cont, "
                                f"Compound, CommitteeNameLiving, Rank, CommitteeNameLiving_cont, Specialty, "
                                f"SpecialAccounting)"
                                f"values {tuple([worker_id] + mil_info)}")
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
                    self.cursor.execute(f"DELETE FROM Education WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Education ("
                                            f"worker_id, UniName, Diploma, GraduationYear, "
                                            f"Specialty, Qualification, EducationForm)"
                                            f"VALUES {tuple([worker_id] + row)}")
                elif table_number == 2:
                    self.cursor.execute(f"DELETE FROM PostGraduationEducation WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(f"INSERT INTO PostGraduationEducation ("
                                            f"worker_id, PostGradUniName, "
                                            f"PostGradDiploma, PostGradGradYear, PostGradDegree)"
                                            f"VALUES {tuple([worker_id] + row)}")
                elif table_number == 3:
                    self.cursor.execute(f"DELETE FROM Family WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Family (worker_id, member, PIB, BirthDate) VALUES "
                                            f"{tuple([worker_id] + row)}")
            else:
                if table_number == 0:
                    self.cursor.execute(f"DELETE FROM ProfessionalEducation WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(
                            f"INSERT INTO ProfessionalEducation(worker_id, Date, Name, Period, Type, Form,Document)"
                            f"VALUES {tuple([worker_id] + row)}")
                elif table_number == 1:
                    self.cursor.execute(f"DELETE FROM Appointment WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Appointment (worker_id, Date, Name, ProfName, Code, "
                                            f"Salary, OrderBasis, Sign) VALUES {tuple([worker_id] + row)}")
                elif table_number == 2:
                    self.cursor.execute(f"DELETE FROM Vacation WHERE worker_id = {worker_id}")
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Vacation(worker_id, Type, Period, Start, End, OrderBasis)"
                                            f"VALUES {tuple([worker_id] + row)}")
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
            self.cursor.execute(f"insert into Workers(id, LastName, FirstName, Patronymic, BirthDate, Photo, unit_name)"
                                f"values ({output}, '', '', '', '', '', '')")
            self.connection.commit()
            return output
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def upload_image(self, worker_id, image_data):
        try:
            self.cursor.execute(f"update Workers set Photo = ? where id={worker_id}",
                                (sqlite3.Binary(image_data),))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def delete_worker(self, worker_id):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute(f"select name from sqlite_master where type='table' and name!='WorkersProjects'")
            tables = self.cursor.fetchall()
            print(tables)
            for x in tables:
                self.cursor.execute(f"pragma table_info({x[0]})")
                self.cursor.execute(f"delete from {x[0]} where {self.cursor.fetchall()[0][1]}={worker_id}")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_worker_projects(self, worker_id):
        self.cursor.execute(f"select * from WorkersProjects where MainWorker_id = {worker_id}")
        return self.cursor.fetchall()

    def get_all_projects(self):
        self.cursor.execute(f"select * from WorkersProjects order by id")
        return self.cursor.fetchall()

    def get_worker_id(self, last_name, first_name):
        self.cursor.execute(f"select id from Workers where LastName='{last_name}' and FirstName='{first_name}'")
        return self.cursor.fetchone()[0]

    def update_projects_table(self, data):
        try:
            self.connection.execute("begin transaction")
            for row in data:
                self.cursor.execute(f"delete from WorkersProjects where id={row[0]}")
                self.cursor.execute(f'insert into WorkersProjects(mainworker_id, id, name, cost, '
                                    f'start, end, collaborators) '
                                    f'VALUES {tuple([self.get_worker_id(*row[-1].split(",")[0].split())]+row)}')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
            return e

    def update_worker_project_table(self, data, worker_id):
        try:
            self.connection.execute("begin transaction")
            k = 0
            self.cursor.execute(f"select count(*) from WorkersProjects where MainWorker_id = {worker_id}")
            old_rows = self.cursor.fetchone()[0]
            self.cursor.execute(f'delete from WorkersProjects where MainWorker_id = {worker_id}')
            for row in data:
                k += 1
                row = [worker_id] + row
                if k <= old_rows:
                    self.cursor.execute(f'insert into WorkersProjects('
                                        f'mainworker_id, id, name, cost, start, end, collaborators) '
                                        f'VALUES {tuple(row)}')
                else:
                    self.cursor.execute(f'select id from WorkersProjects order by id')
                    row[1] = self.cursor.fetchall()[-1][0] + 1
                    self.cursor.execute(f'insert into WorkersProjects('
                                        f'mainworker_id, id, name, cost, start, end, collaborators) '
                                        f'VALUES {tuple(row)}')
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
                self.cursor.execute(f"select count(*) from Workers where unit_name = '{names[i][0]}'")
                row.append(self.cursor.fetchone()[0])

                self.cursor.execute(f"select projects_id from Units where name = '{names[i][0]}'")
                k = 0
                cost = 0
                projects = self.cursor.fetchone()[0]

                if projects:
                    for p in projects.split(','):
                        self.cursor.execute(f'select End from WorkersProjects where id = {p}')
                        end_date = datetime.datetime.strptime(self.cursor.fetchone()[0], "%d-%m-%Y").date()
                        current_date = datetime.date.today().strftime("%Y-%m-%d")
                        formatted_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
                        if end_date > formatted_date:
                            k += 1

                        self.cursor.execute(f'select Cost from WorkersProjects where id = {p}')
                        cost += self.cursor.fetchone()[0]

                row.append(k)
                row.append(len(projects.split(',')) if projects else 0)
                row.append(cost)
                row.append(projects if projects else None)
                rows.append(row)

            self.cursor.execute(f"delete from Units")
            for row in rows:
                self.cursor.execute(f'insert into Units(Name, WorkersQuantity, UnfinishedProjectsQuantity, '
                                    f'AllProjectsQuantity, TotalCost, projects_id) values (?, ?, ?, ?, ?, ?)',
                                    tuple(row))
            self.connection.commit()
            return rows
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_unit_workers(self, unit_name, sort_by, reverse=False):
        self.cursor.execute(f"select id, {sort_by} from Workers where unit_name = '{unit_name}'")
        elements = [i for i in self.cursor.fetchall()]
        sorted_elements = sorted(elements, key=lambda x: locale.strxfrm(x[1]), reverse=reverse)
        return [i[0] for i in sorted_elements]

    def get_unit_projects(self, unit_name):
        try:
            self.cursor.execute(f"select projects_id from Units where Name = '{unit_name}'")
            projects = self.cursor.fetchone()[0].split(',')
            output = []
            for project in projects:
                self.cursor.execute(f"select id, Name, Cost, Start, End, Collaborators from WorkersProjects "
                                    f"where id = {project}")
                output.append(self.cursor.fetchone())
            return output
        except TypeError:
            pass
        except AttributeError:
            pass

    def get_not_unit_workers(self, unit_name):
        self.cursor.execute(f"select id, LastName, FirstName, Patronymic from Workers "
                            f"where unit_name != '{unit_name}' or unit_name is null")

        not_unit_workers = self.cursor.fetchall()
        workers = []
        for i in not_unit_workers:
            self.cursor.execute(f"select unit_name from Workers where id = {i[0]}")
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
            self.cursor.execute(f"update Workers set unit_name = '{unit_name}' where id = {worker_id}")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def update_units(self, units):
        try:
            self.connection.execute("begin transaction")

            self.cursor.execute("select projects_id from Units")
            projects = [i[0] for i in self.cursor.fetchall()]
            if len(projects) != len(units):
                for i in range(len(units)-len(projects)):
                    projects.append(None)

            self.cursor.execute(f"delete from Units")
            for i in zip(units, projects):
                self.cursor.execute(f"insert into Units values (?, ?, ?, ?, ?, ?)",
                                    (i[0], None, None, None, None, i[1]))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_id_of_workers_sorted_by(self, sort_by, reverse=False):
        self.cursor.execute(f"select id, {sort_by} from Workers")
        elements = [i for i in self.cursor.fetchall()]
        sorted_elements = sorted(elements, key=lambda x: locale.strxfrm(x[1]), reverse=reverse)
        return [i[0] for i in sorted_elements]

    def get_posts(self):
        try:
            self.connection.execute("begin transaction")
            rows = []
            self.cursor.execute(f'select Post_name from Posts')
            names = self.cursor.fetchall()
            for i in range(len(names)):
                row = [names[i][0]]
                help_count = int()
                self.cursor.execute(f"select Salary_in_one_worker from Posts where Post_name = '{names[i][0]}'")
                help_salary = self.cursor.fetchone()[0]
                row.append(help_salary)

                self.cursor.execute(f"select Work_time from Posts where Post_name = '{names[i][0]}'")
                row.append(self.cursor.fetchone()[0])

                self.cursor.execute(f"select id from Workers")
                workers_id = [j[0] for j in self.cursor.fetchall()]
                for j in workers_id:
                    self.cursor.execute(f"select Date, Name from Appointment where worker_id = {j}")
                    help = self.cursor.fetchall()
                    sorted_help = sorted(help, key=lambda x: x[0])
                    if sorted_help[-1][1] == names[i][0]:
                        help_count += 1
                row.append(help_count)

                row.append(help_count * help_salary)

                rows.append(row)

            for row in rows:
                self.cursor.execute(f"delete from Posts where Post_name = '{row[0]}'")
                self.cursor.execute(f'insert into Posts(Post_name, Salary_in_one_worker, Work_time, '
                                    f'Sum_of_workers, Sum_salary) values {tuple(row)}')
            self.connection.commit()
            return rows
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def write_post(self, tables_elements):
        try:
            self.connection.execute("begin transaction")
            for i in tables_elements:
                self.cursor.execute(f"delete from Posts where Post_name = '{i[0]}'")
                self.cursor.execute(f'insert into Posts(Post_name, Salary_in_one_worker, Work_time, '
                                    f'Sum_of_workers, Sum_salary) values {tuple(i)}')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()

    def get_projects_for_unit(self):
        self.cursor.execute(f"select Name from WorkersProjects")
        return [i[0] for i in self.cursor.fetchall()]

    def get_project_data_by_name(self, name):
        self.cursor.execute(f"select * from WorkersProjects where Name = '{name}'")
        return self.cursor.fetchone()[1:]

    def set_unit_projects(self, projects, unit_name):
        try:
            self.connection.execute("begin transaction")
            self.cursor.execute(f"update Units set projects_id='{projects}' where Name='{unit_name}'")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
