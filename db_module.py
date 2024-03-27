import json
import mysql.connector
from tkinter import Tk
from tkinter.messagebox import showerror

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    root = Tk()
    root.withdraw()
    showerror("Помилка", "Відсутній файл з налаштуванням підключення до БД.")
    exit()

try:
    mydb = mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    mydb = None
    root = Tk()
    root.withdraw()
    showerror("Помилка при підключенні до БД", f"{err}")
    exit()


def close_connection():
    try:
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        showerror("Помилка підключення БД", f"{err}")


def get_all_workers():
    try:
        mycursor.execute("SELECT * FROM workers")
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        showerror("Помилка підключення БД", f"{err}")


def delete_worker(worker_id):
    try:
        mycursor.execute(f"DELETE FROM workers WHERE id = {worker_id}")
        mydb.commit()
    except mysql.connector.Error as err:
        showerror("Помилка підключення БД", f"{err}")


# print(get_all_workers())
