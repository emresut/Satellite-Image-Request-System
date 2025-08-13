import requests

session = requests.Session()

login_url = "http://localhost:5000/login"
login_data = {
    "username": "example",
    "password": "example"
}

login_response = session.post(login_url, json = login_data)

if login_response.status_code == 200:
    print("Login successful!")

    all_image_requests_url = "http://localhost:5000/all_image_requests"

    response = session.get(all_image_requests_url)
    print("Status code:", response.status_code)
    print("Incoming Response:", response.json())
else:
    print("Status code:", login_response.status_code)
    print("Login failed:", login_response.json())