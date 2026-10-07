import requests

BASE = "http://api.odyssey.test"


class LibraryClient:
    def __init__(self, base, token):
        self.base = base
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer " + token})

    def create(self, book):
        r = self.session.post(self.base + "/books", json=book)
        return r.json()["id"]

    def change(self, book_id, fields):
        r = self.session.patch(self.base + "/books/" + str(book_id), json=fields)
        return r.json()

    def read(self, book_id):
        r = self.session.get(self.base + "/books/" + str(book_id))
        if r.status_code == 404:
            return None
        return r.json()

    def remove(self, book_id):
        return self.session.delete(self.base + "/books/" + str(book_id)).status_code


client = LibraryClient(BASE, "letmein")
new_id = client.create({"title": "Kindred", "price": 11.5})
print("created:", new_id)
print("changed price:", client.change(new_id, {"price": 9.0})["price"])
book = client.read(new_id)
print("read:", book["title"], book["price"])
print("remove:", client.remove(new_id))
print("read after remove:", client.read(new_id))
