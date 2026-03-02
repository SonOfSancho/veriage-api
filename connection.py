import requests
import network_as_code as nac
from dotenv import load_dotenv
import os

load_dotenv()

# Print full response

key = os.getenv("API_KEY")
prueba = "+99999991000"
simprueba = "+34640197653"
simdata = {
"idDocument": "OJAZ00936",
"name": "JOHN OPENTEST",
"givenName": "JOHN", 
"familyName": "OPENTEST",
"familyNameAtBirth": "",
"address": "DEL CLUB DEPORTIVO 1 28223",
"streetName": "DEL CLUB DEPORTIVO",
"streetNumber": "1",
"postalCode": "28223",
"region": "MADRID",
"locality": "POZUELO DE ALARCON",
"country": "ES",
"birthdate":"1976-04-16",
"email": "roberto.garcia@masorange.es",
"gender": "MALE"}
num = 240

client = nac.NetworkAsCodeClient(token=key)

def testcorrect(ans, res):
    print("Correct")
    print("Status Code: ", ans.status_code)
    print("Raw Response: ", ans.text)
    print("Resultado: ", res)

def testincorrect(ans):
    print("Incorrect")
    print("Status Code: ", ans.status_code)


def swapverif(phone):
    url = "https://network-as-code.p-eu.rapidapi.com/passthrough/camara/v1/sim-swap/sim-swap/v0/check"
    payload = {"phoneNumber": phone, "maxAge": num}
    headers = {"Content-Type": "application/json", "x-rapidapi-host": "network-as-code.nokia.rapidapi.com", "x-rapidapi-key": key}
    ans = requests.post(url, json=payload, headers=headers)
    if (ans.status_code == 200):
        data = ans.json()
        res = data.get("swapped")
        return(res)
    else:
        return(-1)

def ageverif(phone):
    data = client.kyc.verify_age(phone_number=phone, age_threshold=18)
    return(data.age_check)

print(swapverif(prueba))
print(ageverif(prueba))
