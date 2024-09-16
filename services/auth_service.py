import random
import string
from datetime import datetime, timedelta
import time
import threading
import os
from functools import wraps
from flask import request, jsonify
from data_access.user_repository import users
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from services import send_sms_service, send_email_service

verification_data = {}


def is_user_exist(identifier: str, identifier_type: str):
    user = None
    if identifier_type == 'email':
        print(users)
        user = next((user for user in users if user.email == identifier), None)
    if identifier_type == 'phone':
        user = next((user for user in users if user.phone == identifier), None)
    return user


def generate_verification_code():
    digits_length = 5
    letters_length = 3
    digits = string.digits
    letters = string.ascii_letters
    random_digits = ''.join(random.choice(digits) for digit in range(digits_length))
    random_letters = ''.join(random.choice(letters) for letter in range(letters_length))
    random_code = random_digits + random_letters
    random_code = ''.join(random.sample(random_code, len(random_code)))
    return random_code


def verify_user(identifier, identifier_type):
    code = generate_verification_code()
    expiration_time = datetime.now() + timedelta(minutes=10)
    verification_data[identifier] = {'code': code, 'expires_at': expiration_time}
    if identifier_type == 'email':
        send_email_service.send_email(identifier, code)
    if identifier_type == 'phone':
        send_sms_service.send_sms(identifier, code)
    return code


def clean_expired_codes():
    current_time = datetime.fromtimestamp(time.time())
    expired_users = [user_id for user_id, data in verification_data.items() if data['expires_at'] < current_time]
    for user_id in expired_users:
        del verification_data[user_id]
    threading.Timer(60, clean_expired_codes).start()


def verify_code_and_create_token(identifier, code):
    if identifier in verification_data:
        data = verification_data[identifier]
        expires_at = data['expires_at']
        current_time = datetime.fromtimestamp(time.time())
        if data['code'] == code and expires_at > current_time:
            token = manage_token(identifier)
            return token
        return "code is not valid"
    return "identifier not found"


def manage_token(identifier):
    secret_key = os.getenv('SECRET_KEY')
    user = next((usr for usr in users if usr.phone == identifier or usr.email == identifier), None)
    token = ""
    if user:
        payload = {
            'caseNumber': user.caseNumber,
            'email': user.email,
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }
        token = generate_token(secret_key, payload)
    return token


def generate_token(secret_key, payload):
    if 'expires_at' in payload:
        payload['expires_at'] = payload['expires_at'].isoformat()
    token = jwt.encode({'user': payload}, secret_key, os.getenv('TOKEN_ALGORITHM'))
    return token


def decode_token(token):
    secret_key = os.getenv('SECRET_KEY')
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    try:
        payload = jwt.decode(token, secret_key, algorithms=[os.getenv('TOKEN_ALGORITHM')])
        return payload['user']
    except ExpiredSignatureError:
        raise ValueError('Token has expired')
    except InvalidTokenError:
        raise ValueError('Invalid token')
    except Exception as e:
        raise ValueError(f'Error decoding token: {str(e)}')


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            payload = decode_token(token)
        except ValueError as e:
            return jsonify({'error': str(e)}), 401

        return f(*args, **kwargs, user=payload)

    return decorator
