import requests

BASE = "http://api.odyssey.test"

# diagnose(path): "too slow", "ok", "need permission", "not found", "server error", "other"


paths = ["/books/1", "/books/0", "/stats", "/broken", "/slow", "/me"]
