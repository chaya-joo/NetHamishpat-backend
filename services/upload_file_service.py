import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from data_access.file_repository import add_file_to_db

load_dotenv()

UPLOAD_FOLDER = os.getenv('DOCUMENTS_STORAGE_PATH')
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}


def is_valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file_and_add_to_db(file, case_number):
    try:
        file_path = save_file(file, case_number)
        if file_path:
            add_to_db(file_path, case_number)
        else:
            raise ValueError("File save failed.")
    except Exception as e:
        raise RuntimeError(f"Error occurred while saving file or adding to DB: {e}")


def save_file(file, case_number):
    try:
        if file and is_valid_file(file.filename):
            filename = secure_filename(file.filename)
            folder_path = os.path.join(UPLOAD_FOLDER, str(case_number))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
            return file_path
        return None
    except Exception as e:
        raise RuntimeError(f"Error saving file: {e}")


def add_to_db(file_path, case_number):
    try:
        add_file_to_db(file_path, case_number)
        print("File added to DB successfully.")
    except Exception as e:
        raise RuntimeError(f"Error adding file to DB: {e}")