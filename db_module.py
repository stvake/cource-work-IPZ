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
    cursor.execute(f"""SELECT Workers.*, FullInfo.Birthplace, FullInfo.Education, FullInfo.Languages
                    FROM Workers JOIN FullInfo ON Workers.id = FullInfo.worker_id WHERE Workers.id = {worker_id}""")
    return cursor.fetchall()


# print(get_all_workers())
# print(get_worker_full_info(1))
