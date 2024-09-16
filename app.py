from flask import Flask, request, jsonify
from flask_cors import CORS
from services.auth_service import is_user_exist, decode_token
from services.auth_service import clean_expired_codes
from services.auth_service import verify_user
from services.auth_service import verify_code_and_create_token
from services.upload_file_service import save_file_and_add_to_db
from dotenv import load_dotenv
from services.auth_service import token_required


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

clean_expired_codes()

load_dotenv()


@app.route('/verifyUser', methods=['POST'])
def check_user():
    data = request.json
    identifier = data.get('identifier')
    identifier_type = data.get('identifier_type')

    if not identifier or not identifier_type:
        return jsonify({'message': 'Missing identifier or identifier_type'}), 400

    user = is_user_exist(identifier, identifier_type)
    if user:
        code = verify_user(identifier, identifier_type)
        return jsonify({'message': 'User exists', 'code': code}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/verifyCode',  methods=['POST'])
def check_code():
    data = request.json
    identifier = data.get('identifier')
    code = data.get('code')
    token = verify_code_and_create_token(identifier, code)
    return jsonify({"message": "success", 'token': token})


@app.route('/uploadFile', methods=['POST'])
@token_required
def add_file(user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    save_file_and_add_to_db(file, user['caseNumber'])
    return "aaa"


@app.route('/check_token',  methods=['GET'])
@token_required
def chece_token(user):
    return jsonify({'user': user})


if __name__ == '__main__':
    app.run(debug=True)
