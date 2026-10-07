import requests

BASE = "http://api.odyssey.test"


def search(author, tag, sort):
    params = {"author": author, "tag": tag, "sort": sort, "per_page": 20}
    books = requests.get(BASE + "/books", params=params).json()["data"]
    return [book["title"] for book in books]


for args in [("Woolf", None, None), (None, "fantasy", None), ("Lem", None, "-year"), ("nobody", None, None)]:
    titles = search(*args)
    if titles:
        print(", ".join(titles))
    else:
        print("nothing found")
