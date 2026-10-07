import requests

BASE = "http://api.odyssey.test"

# offset=0, limit=8; after each request offset += limit; stop when offset >= total
# Each request: "offset 0 -> 8 books"; at the end "total: 23"
