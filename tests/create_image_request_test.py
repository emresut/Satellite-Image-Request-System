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

    create_image_request_url = "http://localhost:5000/create_image_request"
    data = {
        "request_type" : "example",
        "recurring image outer loop duration" : "example",
        "inner loop duration per outer loop" : "example",
        "outer loop start date" : "example",
        "outer loop end date" : "example",
        "inner loop start date" : "example",
        "inner loop end date" : "example",
    }

    response = session.post(create_image_request_url, json = data)
    print("Status code:", response.status_code)
    print("Incoming Response:", response.json())
else:
    print("Status code:", login_response.status_code)
    print("Login failed:", login_response.json())