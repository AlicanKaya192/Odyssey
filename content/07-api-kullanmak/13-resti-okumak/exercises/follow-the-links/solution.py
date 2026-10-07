import requests

BASE = "http://api.odyssey.test"

links = requests.get(BASE + "/").json()["links"]
print(links)

books = requests.get(BASE + links["books"]).json()
print("books:", books["meta"]["total"])

authors = requests.get(BASE + links["authors"]).json()
print("authors:", len(authors["data"]))
