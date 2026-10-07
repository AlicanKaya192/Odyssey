import requests

BASE = "http://api.odyssey.test"
TOKEN = "letmein"

r = requests.get(BASE + "/me", headers={"Authorization": TOKEN})
print("no prefix:", r.status_code)

r = requests.get(BASE + "/me", headers={"Authorization": "Bearer " + TOKEN})
me = r.json()
print("with Bearer:", r.status_code)
print("user:", me["user"])
print("role:", me["role"])
