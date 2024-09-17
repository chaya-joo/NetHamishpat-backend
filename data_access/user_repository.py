import os
import pypyodbc as odbc
from models.user_model import User
from dotenv import load_dotenv

load_dotenv()


def get_all_users():
    try:
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

        return users

    except Exception as e:
        raise RuntimeError(f"Error occurred while retrieving users: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        del cursor
        del conn


users = get_all_users()
