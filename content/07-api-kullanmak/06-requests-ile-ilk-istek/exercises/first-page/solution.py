import requests

response = requests.get("http://api.odyssey.test/books")
body = response.json()

titles = []
for book in body["data"]:
    titles.append(book["title"])

print("total:", body["meta"]["total"])
print("on this page:", len(titles))
for title in titles:
    print(title)
