import xmltodict
from flask import Flask, request, jsonify
from flask_cors import CORS
from requests import Session


from services.auth_service import is_user_exist, decode_token
from services.auth_service import clean_expired_codes
from services.auth_service import verify_user
from services.auth_service import verify_code_and_create_token
from services.upload_file_service import save_file_and_add_to_db
from dotenv import load_dotenv
from services.auth_service import token_required
from data_access.soap_client import calculate
from zeep import Client, Settings, Transport

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

clean_expired_codes()

load_dotenv()


@app.route('/verifyUser', methods=['POST'])
def check_user():
    try:
        data = request.json
        if not data:
            raise ValueError("Request body is missing")
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
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/verifyCode', methods=['POST'])
def check_code():
    try:
        data = request.json
        if not data:
            raise ValueError("Request body is missing")
        identifier = data.get('identifier')
        code = data.get('code')
        if not identifier or not code:
            return jsonify({'message': 'Missing identifier or code'}), 400
        token = verify_code_and_create_token(identifier, code)
        return jsonify({"message": "success", 'token': token}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/uploadFile', methods=['POST'])
@token_required
def add_file(user):
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        save_file_and_add_to_db(file, user['caseNumber'])
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/getDecision', methods=['POST']) #רשימת החלטות
@token_required
def get_decision(user):
    wsdl = 'https://secure.court.gov.il/NGCS.SoftwareCompaniesInterfaces.SI/DecisionSI.asmx?WSDL'
    case_id = user.caseNumber
    session = Session()  # מאפשר להגדיר פרטי חיבור ואימות
    session.auth = ('username', 'password')
    transport = Transport(session=session)  #מגדיר את אופן החיבור עם השרת
    client = Client(wsdl=wsdl, transport=transport)
    header = {
        'RequestId': '123',
        'UserType': 'תז',
        'UserId': '0535321054',
    }
    client.transport = Transport(session=session)
    request_params = {
        'CaseIdentification': {
            'CaseID': case_id
        }
    }
    try:
        response = client.service.GetDecisionsByCaseID(  #לשנות את שם הפונקציה!!
            CaseIdentification=request_params['CaseIdentification'],
            _soapheaders=header
        )

        response_dict = xmltodict.parse(response)
        response_json = jsonify(response_dict)
        print(response_json)
        return response_json

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/getSittings', methods=['POST'])
@token_required
def get_sittings(user):
    wsdl = 'https://secure.court.gov.il/NGCS.SoftwareCompaniesInterface.SI/MeetingSI.asmx?WSDL'
    case_id = user.caseNumber
    session = Session()  # מאפשר להגדיר פרטי חיבור ואימות
    session.auth = ('username', 'password')
    transport = Transport(session=session)  #מגדיר את אופן החיבור עם השרת
    client = Client(wsdl=wsdl, transport=transport)
    header = {
        'RequestId': '123',
        'UserType': 'תז',
        'UserId': '0535321054',
    }
    request_params = {
        'CaseIdentification': {
            'CaseID': case_id
        }
    }
    try:
        response = client.service.GetSittingsByCaseID(  #לשנות את שם הפונקציה!!
            CaseIdentification=request_params['CaseIdentification'],
            _soapheaders=header
        )

        response_dict = xmltodict.parse(response)
        response_json = jsonify(response_dict)
        print(response_json)
        return response_json

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/checkWebService', methods=['POST'])
def check_web_service():
    data = request.json
    num1 = data.get('num1')
    num2 = data.get('num2')
    return calculate(num1, num2)


if __name__ == '__main__':
    app.run(debug=True)
