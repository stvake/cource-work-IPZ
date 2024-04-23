import sqlite3

connection = sqlite3.connect('HumanResourceDepartment.db')
cursor = connection.cursor()


def get_workers_quantity():
    cursor.execute('SELECT COUNT(*) FROM Workers')
    return cursor.fetchone()[0]


def get_worker_info(worker_id):
    cursor.execute(f"SELECT * FROM Workers WHERE id = {worker_id}")
    return cursor.fetchall()


def delete_worker(worker_id):
    cursor.execute(f"DELETE FROM Workers WHERE id = {worker_id}")
    connection.commit()


def get_worker_full_info(worker_id):
    output = []

    cursor.execute(f""" SELECT * FROM Workers JOIN FullInfo ON
    Workers.id = FullInfo.worker_id WHERE Workers.id = {worker_id}""")
    info = cursor.fetchall()[0]
    temp = []
    for el in range(len(info)):
        if el != 0 and el != 4 and el != 6 and el != 8:
            temp.append(info[el])
    output.append(temp)

    cursor.execute(f"""SELECT * FROM Education WHERE Education.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    cursor.execute(f"""SELECT * FROM PostGraduationEducation WHERE PostGraduationEducation.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    cursor.execute(f"""SELECT * FROM Family WHERE Family.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    cursor.execute(f"""SELECT * FROM Military WHERE Military.worker_id = {worker_id}""")
    output.append(cursor.fetchall()[0][1:])

    cursor.execute(f"""SELECT * FROM ProfessionalEducation WHERE ProfessionalEducation.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    cursor.execute(f"""SELECT * FROM Appointment WHERE Appointment.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    cursor.execute(f"""SELECT * FROM Vacation WHERE Vacation.worker_id = {worker_id}""")
    output.append(cursor.fetchall())

    return output


def update_info(worker_id, info):
    cursor.execute("PRAGMA table_info(Workers)")
    columns = [column[1] for column in cursor.fetchall() if column[1] not in ['id', 'Email', 'Post', 'Photo']]
    cursor.execute("PRAGMA table_info(FullInfo)")
    columns.extend(column[1] for column in cursor.fetchall() if column[1] != 'worker_id')

    new_info = [i for i in zip(columns, info)]

    for i in range(len(new_info)):
        if i <= 3:
            cursor.execute(f"UPDATE Workers SET {new_info[i][0]}='{new_info[i][1]}' WHERE id = {worker_id}")
            connection.commit()
        elif i > 3:
            cursor.execute(f"UPDATE FullInfo SET {new_info[i][0]}='{new_info[i][1]}' WHERE worker_id = {worker_id}")
            connection.commit()


def update_table(worker_id, tables_list, table_number, data):
    if tables_list == 0:
        if table_number == 0:
            cursor.execute(f"DELETE FROM Education WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO Education "
                               f"(worker_id, UniName, Diploma, GraduationYear, Specialty, Qualification, EducationForm)"
                               f"VALUES {tuple([worker_id] + row)}")
                connection.commit()
        elif table_number == 2:
            cursor.execute(f"DELETE FROM PostGraduationEducation WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO PostGraduationEducation (worker_id, PostGraduate, PostGradUniName, "
                               f"PostGradDiploma, PostGradGradYear, PostGradDegree) VALUES {tuple([worker_id] + row)}")
                connection.commit()
        elif table_number == 3:
            cursor.execute(f"DELETE FROM Family WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO Family (worker_id, member, PIB, BirthDate) VALUES "
                               f"{tuple([worker_id] + row)}")
                connection.commit()
    else:
        if table_number == 0:
            cursor.execute(f"DELETE FROM ProfessionalEducation WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO ProfessionalEducation(worker_id, Date, Name, Period, Type, Form, Document)"
                               f"VALUES {tuple([worker_id] + row)}")
                connection.commit()
        elif table_number == 1:
            cursor.execute(f"DELETE FROM Appointment WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO Appointment (worker_id, Date, Name, ProfName, Code, Salary, "
                               f"OrderBasis, Sign) VALUES {tuple([worker_id] + row)}")
                connection.commit()
        elif table_number == 2:
            cursor.execute(f"DELETE FROM Vacation WHERE worker_id = {worker_id}")
            connection.commit()
            for row in data:
                cursor.execute(f"INSERT INTO Vacation (worker_id, Type, Period, Start, End, OrderBasis) VALUES "
                               f"{tuple([worker_id] + row)}")
                connection.commit()
