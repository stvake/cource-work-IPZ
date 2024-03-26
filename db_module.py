import json
import mysql.connector

with open('config.json', 'r') as f:
    config = json.load(f)

mydb = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

mycursor = mydb.cursor()


def get_all_workers():
    mycursor.execute("SELECT * FROM workers")
    return mycursor.fetchall()


def delete_worker(worker_id):
    mycursor.execute(f"DELETE FROM workers WHERE id = {worker_id}")
    mydb.commit()


# print(get_all_workers())
