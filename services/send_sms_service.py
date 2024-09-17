import requests
from dotenv import load_dotenv
import os
import json

url = 'https://api.sms4free.co.il/ApiSMS/v2/SendSMS'

load_dotenv()


def send_sms(identifier, code):
    try:
        payload = {
            'key': os.getenv('SEND_SMS_API_KEY'),
            'user': os.getenv('SEND_SMS_USER'),
            'pass': os.getenv('SEND_SMS_PASSWORD'),
            'sender': os.getenv('SEND_SMS_SENDER'),
            'recipient': identifier,
            'msg': f'{code} הונפק עבורך קוד האימות הבא:\nהקוד תקף ל-10 דקות'
        }
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()  # Check if request was successful
        response_json = response.json()
        status = response_json.get('status')
        message = response_json.get('message')

        print(f"Status: {status}")
        print(f"Message: {message}")
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to send SMS: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred: {e}")
