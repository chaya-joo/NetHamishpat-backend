from dotenv import load_dotenv
import pypyodbc as odbc
import os

from pypyodbc import Connection

load_dotenv()


def get_conn():
    server = os.getenv('SERVER')
    server_name = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE_NAME')
    connection_string = f'DRIVER={{{server}}};SERVER={server_name};DATABASE={database};TrustConnection=yes'
    conn = odbc.connect(connection_string)
    conn.close()
    return conn


conn = get_conn()

