import requests

BASE = "http://api.odyssey.test"

classics = []
pages = 0
url = BASE + "/books?tag=classic&per_page=4"
while url:
    body = requests.get(url).json()
    pages += 1
    classics.extend(body["data"])
    nxt = body["links"]["next"]
    if nxt:
        print("next:", nxt)
        url = BASE + nxt
    else:
        url = None

print("pages:", pages)
print("classics:", len(classics))
