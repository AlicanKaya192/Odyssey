import json
import urllib.request

data = json.load(urllib.request.urlopen("http://api:8000/", timeout=3))
print("items:", data["items"], flush=True)
