import requests

BASE = "http://api.odyssey.test"


def fetch_all():
    titles = []
    cursor = None
    while True:
        params = {"cursor": cursor} if cursor else {}
        body = requests.get(BASE + "/cursor/books", params=params).json()
        titles.extend(book["title"] for book in body["results"])
        cursor = body["next_cursor"]
        if cursor is None:
            return titles


titles = fetch_all()
print("books:", len(titles))
print("first:", titles[0])
print("last:", titles[-1])
