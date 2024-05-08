import sqlite3
import datetime


class HandleDataBaseModel:
    def __init__(self):
        self.connection = sqlite3.connect('HumanResourceDepartment.db')
        self.cursor = self.connection.cursor()

    def get_workers_quantity(self):
        self.cursor.execute('SELECT id FROM Workers order by id')
        return self.cursor.fetchall()[-1][0]

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

    def if_exists(self, table, column, worker_id):
        self.cursor.execute(f"SELECT 1 FROM {table} WHERE {column} = ?", (worker_id,))
        return self.cursor.fetchone()

    def update_info(self, worker_id, info, mil_info):
        try:
            self.connection.execute("begin transaction")
            if self.if_exists('Workers', 'id', worker_id):
                self.cursor.execute(f"delete from Workers where id = {worker_id}")
                self.cursor.execute(f"delete from FullInfo where worker_id = {worker_id}")
                self.cursor.execute(f"delete from Military where worker_id = {worker_id}")

            self.cursor.execute(f"insert into Workers (id, LastName, FirstName, Patronymic, BirthDate)"
                                f"values {tuple([worker_id] + info[0:4])}")
            self.cursor.execute(f"update Workers set Photo = ? where id={worker_id}",
                                (sqlite3.Binary(info[4]),))
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
            self.cursor.execute(f"insert into Workers (id, LastName, FirstName, Patronymic, BirthDate, Photo, unit_id) "
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

    def update_projects_table(self, data):
        try:
            self.connection.execute("begin transaction")
            for row in data:
                self.cursor.execute(f'insert into WorkersProjects(mainworker_id, id, name, cost, start, end, '
                                    f'collaborators) VALUES {tuple(row)}')
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
            rows = []
            self.cursor.execute(f'select id from Units')
            ids = self.cursor.fetchall()
            for i in range(len(ids)):
                row = []
                self.cursor.execute(f'select id, Name from Units')
                row.extend([j for j in self.cursor.fetchall()[i]])
                self.cursor.execute(f'select count(*) from Workers where unit_id = {ids[i][0]}')
                row.append(self.cursor.fetchone()[0])

                self.cursor.execute(f'select projects_id from Units where id = {ids[i][0]}')
                k = 0
                cost = 0
                projects = self.cursor.fetchone()[0]

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
                row.append(len(projects.split(',')))
                row.append(cost)
                rows.append(row)

            return rows
        except sqlite3.Error as e:
            print(f"\033[91m{e}\033[0m")
            self.connection.rollback()
