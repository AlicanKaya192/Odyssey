import json
import time
import urllib.request

API_URL = "http://api:8000/"

while True:
    try:
        data = json.load(urllib.request.urlopen(API_URL, timeout=3))
        print("items:", data["items"], flush=True)
        break
    except OSError as error:
        print("waiting for the API:", error, flush=True)
        time.sleep(1)

time.sleep(300)
