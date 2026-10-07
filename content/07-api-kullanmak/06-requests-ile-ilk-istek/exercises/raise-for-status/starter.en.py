import requests

BASE = "http://api.odyssey.test"
paths = ["/books/5", "/books/0", "/authors/3", "/authors/42"]

# For each address: request + raise_for_status(); try/except requests.HTTPError
