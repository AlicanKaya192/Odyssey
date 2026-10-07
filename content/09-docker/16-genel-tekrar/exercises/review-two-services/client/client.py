import json
import urllib.request

with urllib.request.urlopen("http://api:8000/stats", timeout=5) as response:
    stats = json.load(response)
print("notes:", stats["notes"], "starts:", stats["starts"])
