import requests

BASE = "http://api.odyssey.test"

books = []
page = 1
requests_sent = 0
while True:
    body = requests.get(BASE + "/books", params={"page": page}).json()
    requests_sent += 1
    books.extend(body["data"])
    if page >= body["meta"]["pages"]:
        break
    page += 1

print("books:", len(books))
print("requests:", requests_sent)
for book in books[-3:]:
    print(book["title"])
