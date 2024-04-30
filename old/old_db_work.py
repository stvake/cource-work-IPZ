import sqlite3

connection = sqlite3.connect('../HumanResourceDepartment.db')
cursor = connection.cursor()

# with open("./photos/placeholder_photo.png", "rb") as file:
#     image_data = file.read()
#
# cursor.execute("UPDATE Workers SET Photo = ?", (sqlite3.Binary(image_data),))
#
# connection.commit()

connection.close()
