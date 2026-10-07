import requests

BASE = "http://api.odyssey.test"

author_id = None
for author in requests.get(BASE + "/authors").json()["data"]:
    if author["name"] == "Le Guin":
        author_id = author["id"]

books = requests.get(BASE + "/authors/" + str(author_id) + "/books").json()["data"]
print("author id:", author_id)
print("books:", len(books))
for book in books:
    print(book["year"], book["title"])
