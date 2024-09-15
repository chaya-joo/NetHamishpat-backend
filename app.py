import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.auth_service import is_user_exist, decode_token
from services.auth_service import clean_expired_codes
from services.auth_service import verify_user
from services.auth_service import is_code_valid
import subprocess
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

clean_expired_codes()

subprocess.run(['python', 'scripts/generate_secret_key.py'])

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
    token = is_code_valid(identifier, code)
    return jsonify({"message": "success", 'token': token})


@app.route('/decode_token',  methods=['GET'])
def decode():
    token = request.json.get('token')
    return decode_token(token)


if __name__ == '__main__':
    app.run(debug=True)
