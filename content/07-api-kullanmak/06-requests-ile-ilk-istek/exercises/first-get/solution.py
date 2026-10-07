import requests

response = requests.get("http://api.odyssey.test/books/1")
book = response.json()

print("status:", response.status_code)
print("ok:", response.ok)
print("title:", book["title"])
print("author:", book["author"]["name"])
