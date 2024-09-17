import xmltodict
from zeep import Client


def calculate(num1, num2):
    wsdl = 'http://www.dneonline.com/calculator.asmx?WSDL'
    client = Client(wsdl=wsdl)
    result = client.service.Add(num1, num2)
    if isinstance(result, str):
        return result
    else:
        return f"result is: {result}"



def weather():
    wsdl = 'http://www.webservicex.net/globalweather.asmx?WSDL'

    client = Client(wsdl=wsdl)

    city = 'Tel Aviv'
    country = 'Israel'
    response = client.service.GetWeather(city, country)
    return response
