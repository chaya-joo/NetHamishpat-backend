import xmltodict
from zeep import Client


def calculate(num1, num2):
    wsdl = 'http://www.dneonline.com/calculator.asmx?WSDL'
    client = Client(wsdl=wsdl)
    result = client.service.Add(num1, num2)
    if isinstance(result, str):
        return xmltodict.parse(result)
    else:
        return f"result is: {result}"
