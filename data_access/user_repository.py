import os
import pypyodbc as odbc
from models.user_model import User
from dotenv import load_dotenv

load_dotenv()


def get_all_users():
    server = os.getenv('SERVER')
    server_name = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE_NAME')
    connection_string = f'DRIVER={{{server}}};SERVER={server_name};DATABASE={database};TrustConnection=yes'
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    query = 'SELECT * FROM Users'
    cursor.execute(query)
    rows = cursor.fetchall()
    users = [User(row) for row in rows]
    cursor.close()
    conn.close()
    return users


users = get_all_users()









