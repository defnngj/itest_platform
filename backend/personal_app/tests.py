from django.test import TestCase

# Create your tests here.
import requests

login = requests.post("http://127.0.0.1:8000/api/personal/v1/login/", data={"username": "admin", "password": "admin123456"})
login_token = login.json()["data"]["Token"]
print("token", login_token)

header = {"token": login_token}
user = requests.get("http://127.0.0.1:8000/api/personal/v1/user/", headers=header)
print(user.json())
