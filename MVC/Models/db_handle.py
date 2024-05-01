import sqlite3


class HandleDataBaseModel:
    def __init__(self):
        self.connection = sqlite3.connect('HumanResourceDepartment.db')
        self.cursor = self.connection.cursor()

    def get_workers_quantity(self):
        self.cursor.execute('SELECT COUNT(*) FROM Workers')
        return self.cursor.fetchone()[0]

    def get_worker_info(self, worker_id):
        self.cursor.execute(f"SELECT * FROM Workers WHERE id = {worker_id}")
        info = list(self.cursor.fetchone())
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
            if el != 0 and el != 6:
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
            if self.if_exists('Workers', 'id', worker_id):
                self.cursor.execute(f"delete from Workers where id = {worker_id}")
                self.connection.commit()
                self.cursor.execute(f"delete from FullInfo where worker_id = {worker_id}")
                self.connection.commit()
                self.cursor.execute(f"delete from Military where worker_id = {worker_id}")
                self.connection.commit()

            self.cursor.execute(f"insert into Workers (id, LastName, FirstName, Patronymic, BirthDate)"
                                f"values {tuple([worker_id] + info[0:4])}")
            self.connection.commit()
            self.cursor.execute(f"update Workers set Photo = ? where id={worker_id}",
                                (sqlite3.Binary(info[4]),))
            self.connection.commit()
            self.cursor.execute(f"insert into FullInfo (worker_id, Nationality, Education, LastWork, LastWorkPost, "
                                f"WorkExperienceDate, WorkExperienceDays, WorkExperienceMonths, WorkExperienceYears, "
                                f"WorkBonusDays, WorkBonusMonths, WorkBonusYears, OldFireDate, OldFireReason, Pension, "
                                f"FamilyStatus, ActualResidence, RegisteredResidence, RegisteredResidence_cont, "
                                f"PassportSeries, PassportNumber, PassportIssuedBy, PassportIssueDate, AdditionalInfo, "
                                f"AdditionalInfo_cont, FireDate, FireReason, PersonnelServiceEmployeePost, "
                                f"PersonnelServiceEmployeeSign, PersonnelServiceEmployeePIB, EmployeePIB, EmployeeSign,"
                                f"EmployeeFireDate, EmployeeFireYear)"
                                f"values {tuple([worker_id]+info[5:])}")
            self.connection.commit()
            self.cursor.execute(f"insert into Military (worker_id, AccountingGroup, Suitability, AccountingCategory, "
                                f"CommitteeNameRegistration, AccountingCategory_cont, CommitteeNameRegistration_cont, "
                                f"Compound, CommitteeNameLiving, Rank, CommitteeNameLiving_cont, Specialty, "
                                f"SpecialAccounting)"
                                f"values {tuple([worker_id] + mil_info)}")
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            print(error)

    def update_table(self, worker_id, tables_list, table_number, data):
        try:
            if tables_list == 0:
                if table_number == 0:
                    self.cursor.execute(f"DELETE FROM Education WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Education ("
                                            f"worker_id, UniName, Diploma, GraduationYear, "
                                            f"Specialty, Qualification, EducationForm)"
                                            f"VALUES {tuple([worker_id] + row)}")
                        self.connection.commit()
                elif table_number == 2:
                    self.cursor.execute(f"DELETE FROM PostGraduationEducation WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(f"INSERT INTO PostGraduationEducation ("
                                            f"worker_id, PostGradUniName, "
                                            f"PostGradDiploma, PostGradGradYear, PostGradDegree)"
                                            f"VALUES {tuple([worker_id] + row)}")
                        self.connection.commit()
                elif table_number == 3:
                    self.cursor.execute(f"DELETE FROM Family WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Family (worker_id, member, PIB, BirthDate) VALUES "
                                            f"{tuple([worker_id] + row)}")
                        self.connection.commit()
            else:
                if table_number == 0:
                    self.cursor.execute(f"DELETE FROM ProfessionalEducation WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(
                            f"INSERT INTO ProfessionalEducation(worker_id, Date, Name, Period, Type, Form, Document)"
                            f"VALUES {tuple([worker_id] + row)}")
                        self.connection.commit()
                elif table_number == 1:
                    self.cursor.execute(f"DELETE FROM Appointment WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Appointment (worker_id, Date, Name, ProfName, Code, Salary, "
                                            f"OrderBasis, Sign) VALUES {tuple([worker_id] + row)}")
                        self.connection.commit()
                elif table_number == 2:
                    self.cursor.execute(f"DELETE FROM Vacation WHERE worker_id = {worker_id}")
                    self.connection.commit()
                    for row in data:
                        self.cursor.execute(f"INSERT INTO Vacation (worker_id, Type, Period, Start, End, OrderBasis) "
                                            f"VALUES {tuple([worker_id] + row)}")
                        self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()

    def create_new_worker(self):
        self.cursor.execute("select * from Workers order by id desc")
        output = self.cursor.fetchall()[0][0] + 1
        self.cursor.execute(f"insert into Workers (id, LastName, FirstName, Patronymic, BirthDate, Photo) "
                            f"values ({output}, '', '', '', '', '')")
        self.connection.commit()
        return output

    def upload_image(self, worker_id, image_data):
        try:
            self.cursor.execute(f"update Workers set Photo = ? where id={worker_id}",
                                (sqlite3.Binary(image_data),))
            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()

    def delete_worker(self, worker_id):
        try:
            self.cursor.execute(f"select name from sqlite_master where type='table'")
            for x in self.cursor.fetchall():
                self.cursor.execute(f"delete from {x[0]} where id={worker_id}")
                self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
