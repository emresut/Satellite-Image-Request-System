import requests

url = "http://localhost:5000/register"

data = {
    "username" : "emre3",
    "password" : "123456",
    "confirm_password" : "123456"
}

response = requests.post(url, json = data)
print("Status code:", response.status_code)
try:
    print("Incoming Response:", response.json())
except ValueError:
    print("Raw response (non-JSON):", response.text)