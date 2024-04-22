import sqlite3

connection = sqlite3.connect('HumanResourceDepartment.db')
cursor = connection.cursor()


def get_all_workers():
    cursor.execute("SELECT * FROM Workers")
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


# print(get_all_workers())

# print(get_worker_full_info(1))
# for i in get_worker_full_info(1):
#     print(i)
