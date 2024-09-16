import os
import pypyodbc as odbc
from dotenv import load_dotenv


load_dotenv()


def add_file_to_db(file_path, case_number):
    server = os.getenv('SERVER')
    server_name = os.getenv('SERVER_NAME')
    database = os.getenv('DATABASE_NAME')
    connection_string = f'DRIVER={{{server}}};SERVER={server_name};DATABASE={database};TrustConnection=yes'
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    query = 'INSERT INTO Documents (CaseNumber, FilePath) VALUES (?, ?)'
    cursor.execute(query, (case_number, file_path))
    conn.commit()
    cursor.close()
    conn.close()
    del cursor
    del conn
