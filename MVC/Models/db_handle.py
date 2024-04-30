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
            if el != 0 and el != 4 and el != 7:
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

    def update_info(self, worker_id, info):
        self.cursor.execute("PRAGMA table_info(Workers)")
        columns = [column[1] for column in self.cursor.fetchall() if column[1] not in ['id', 'Email', 'Post', 'Photo']]
        self.cursor.execute("PRAGMA table_info(FullInfo)")
        columns.extend(column[1] for column in self.cursor.fetchall() if column[1] != 'worker_id')

        new_info = [i for i in zip(columns, info)]

        for i in range(len(new_info)):
            if i <= 3:
                self.cursor.execute(f"UPDATE Workers SET {new_info[i][0]}='{new_info[i][1]}' WHERE id = {worker_id}")
                self.connection.commit()
            elif i > 3:
                self.cursor.execute(f"UPDATE FullInfo SET {new_info[i][0]}='{new_info[i][1]}' "
                                    f"WHERE worker_id = {worker_id}")
                self.connection.commit()

    def update_table(self, worker_id, tables_list, table_number, data):
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
