import requests
from dotenv import load_dotenv
import os
import json

url = 'https://api.sms4free.co.il/ApiSMS/v2/SendSMS'

load_dotenv()


def send_SMS(identifier, code):
    payload = {
        'key': os.getenv('SEND_SMS_API_KEY'),
        'user': os.getenv('SEND_SMS_USER'),
        'pass': os.getenv('SEND_SMS_PASSWORD'),
        'sender': os.getenv('SEND_SMS_SENDER'),
        'recipient': identifier,
        'msg': f'{code}הונפק עבורך קוד האימות הבא: '+'\nהקוד תקף ל-10 דקות'
    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
    response_json = response.json()
    status = response_json.get('status')
    message = response_json.get('message')

    print(f"Status: {status}")
    print(f"Message: {message}")
