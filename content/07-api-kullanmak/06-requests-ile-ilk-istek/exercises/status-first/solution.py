import requests

BASE = "http://api.odyssey.test"


def get_title(book_id):
    response = requests.get(BASE + "/books/" + str(book_id))
    if response.status_code == 200:
        return response.json()["title"]
    return None


ids = [4, 99, 12, 0]
for book_id in ids:
    print(book_id, "->", get_title(book_id))
