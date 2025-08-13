import requests

url = "http://localhost:5000/login"

data = {
    "username" : "example",
    "password" : "example"
}

response = requests.post(url, json = data)
print("Status code:", response.status_code)
print("Incoming Response:", response.json())