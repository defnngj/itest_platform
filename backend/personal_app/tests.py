from django.test import TestCase

# Create your tests here.
import requests
header = {"token": "adfasdfasdf"}
r = requests.get("http://127.0.0.1:8000/test/", headers=header)

print(r.text)
