from django.test import TestCase
import requests
from retrying import retry


# Create your tests here.
# @retry(stop_max_attempt_number=3, wait_fixed=1)
def test_get_token():
    data = {"username": "admin", "password": "!@#qwerasdzxc123"}
    url = "http://127.0.0.1:9000/api/user/auth"
    resp = requests.post(url, data=data, timeout=10)
    print(resp.text)
    if resp.status_code == 200:
        print(resp.json())


if __name__ == "__main__":
    test_get_token()