import requests

BASE = "http://api.odyssey.test"

# fetch(url): "ok 200", "timeout", "no connection" ya da "http error 404"


urls = [
    BASE + "/books/1",
    BASE + "/books/0",
    BASE + "/slow",
    "http://offline.odyssey.test/books",
]
# Her adres icin sonucu yazdir
