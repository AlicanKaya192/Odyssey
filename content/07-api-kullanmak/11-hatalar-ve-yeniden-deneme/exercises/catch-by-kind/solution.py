import requests

BASE = "http://api.odyssey.test"


def fetch(url):
    try:
        r = requests.get(url, timeout=1)
        r.raise_for_status()
    except requests.Timeout:
        return "timeout"
    except requests.ConnectionError:
        return "no connection"
    except requests.HTTPError:
        return "http error " + str(r.status_code)
    return "ok " + str(r.status_code)


urls = [
    BASE + "/books/1",
    BASE + "/books/0",
    BASE + "/slow",
    "http://offline.odyssey.test/books",
]
for url in urls:
    print(fetch(url))
