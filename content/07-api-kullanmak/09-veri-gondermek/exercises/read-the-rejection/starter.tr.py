import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

books = [
    {"title": "", "price": 7.0},
    {"title": "Kindred", "price": "11.50"},
    {"title": "Kindred", "price": 11.5, "author_id": 99},
    {"title": "Kindred", "price": 11.5},
]

# Her kitap icin POST; 201 ise "created /books/..", degilse "422 title must be ..."
