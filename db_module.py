import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()


def get_all_workers():
    cursor.execute("SELECT * FROM Workers")
    return cursor.fetchall()


def delete_worker(worker_id):
    cursor.execute(f"DELETE FROM Workers WHERE id = {worker_id}")
    connection.commit()


# print(get_all_workers())
