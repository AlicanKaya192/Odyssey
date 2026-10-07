import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

url = BASE + "/books/12"
print("old price:", requests.get(url).json()["price"])

r = requests.patch(url, json={"price": 5.5}, headers=AUTH)
print("patch:", r.status_code)

book = requests.get(url).json()
print("new price:", book["price"])
print("year:", book["year"])
