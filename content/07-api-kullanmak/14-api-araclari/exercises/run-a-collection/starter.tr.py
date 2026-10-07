import requests

environment = {"base_url": "http://api.odyssey.test", "token": "letmein"}

collection = [
    {"name": "List books", "method": "GET", "url": "{{base_url}}/books", "headers": {}},
    {"name": "Who am I", "method": "GET", "url": "{{base_url}}/me",
     "headers": {"Authorization": "Bearer {{token}}"}},
    {"name": "Add a book", "method": "POST", "url": "{{base_url}}/books",
     "headers": {"Authorization": "Bearer {{token}}"}, "body": {"title": "Kindred", "price": 11.5}},
    {"name": "Missing book", "method": "GET", "url": "{{base_url}}/books/99", "headers": {}},
]

# fill(text, variables): her {{ad}} yerine degeri


# Her istek: "List books: 200"
