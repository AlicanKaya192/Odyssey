import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

new_book = {"title": "The Word for World Is Forest", "author_id": 6, "year": 1972, "price": 9.4}

# POST /books: json=new_book, headers=AUTH


# Yazdir: "status: ...", "location: ...", "id: ...", "author: ..."
