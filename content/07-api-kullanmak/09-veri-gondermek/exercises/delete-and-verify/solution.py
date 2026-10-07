import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

url = BASE + "/books/7"
r = requests.delete(url, headers=AUTH)
print("delete:", r.status_code, "empty body:", r.text == "")

print("get after delete:", requests.get(url).status_code)
print("delete again:", requests.delete(url, headers=AUTH).status_code)
