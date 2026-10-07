import requests

BASE = "http://api.odyssey.test"


def newest(n):
    titles = []
    page = 1
    while len(titles) < n:
        body = requests.get(BASE + "/books", params={"sort": "-year", "per_page": 5, "page": page}).json()
        if not body["data"]:
            break
        titles.extend(book["title"] for book in body["data"])
        page += 1
    return titles[:n]


for title in newest(7):
    print(title)
