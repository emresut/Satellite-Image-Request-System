import requests

session = requests.Session()

login_url = "http://localhost:5000/login"
login_data = {
    "username": "emre2",
    "password": "123456"
}

login_response = session.post(login_url, json = login_data)

if login_response.status_code == 200:
    print("Login successful!")

    create_image_request_url = "http://localhost:5000/create_image_request"
    data = {
        "request_type" : "recurring",
        "recurring image outer loop duration" : "365",
        "inner loop duration per outer loop" : "30",
        "outer loop start date" : "2023-11-25",
        "outer loop end date" : "2027-11-25",
        "inner loop start date" : "2023-11-25",
        "inner loop end date" : "2023-12-25",
    }

    response = session.post(create_image_request_url, json = data)
    print("Status code:", response.status_code)
    print("Incoming Response:", response.json())
else:
    print("Status code:", login_response.status_code)
    print("Login failed:", login_response.json())