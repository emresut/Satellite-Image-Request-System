import requests

url = "http://localhost:5000/login"

data = {
    "username" : "emre2",
    "password" : "123456"
}

response = requests.post(url, json = data)
print("Status code:", response.status_code)
print("Incoming Response:", response.json())