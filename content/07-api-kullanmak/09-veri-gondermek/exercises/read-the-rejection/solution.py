import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

books = [
    {"title": "", "price": 7.0},
    {"title": "Kindred", "price": "11.50"},
    {"title": "Kindred", "price": 11.5, "author_id": 99},
    {"title": "Kindred", "price": 11.5},
]

for book in books:
    r = requests.post(BASE + "/books", json=book, headers=AUTH)
    if r.status_code == 201:
        print("created", r.headers["Location"])
    else:
        print(r.status_code, r.json()["detail"])
