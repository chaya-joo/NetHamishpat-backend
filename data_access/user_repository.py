import os
import pymssql


def get_all_users():
    server = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE_NAME')

    conn = pymssql.connect(server='DESKTOP-5Q9K2NL', database='MyStorageDB', user='user1', password='6865')
    print("connect to db!!")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    conn.close()
    return users
