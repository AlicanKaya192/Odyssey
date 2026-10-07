import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}

books = [
    {"title": "", "price": 7.0},
    {"title": "Kindred", "price": "11.50"},
    {"title": "Kindred", "price": 11.5, "author_id": 99},
    {"title": "Kindred", "price": 11.5},
]

# POST each book; on 201 "created /books/..", otherwise "422 title must be ..."
