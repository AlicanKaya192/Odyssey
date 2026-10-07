import requests

BASE = "http://api.odyssey.test"

# offset=0, limit=8; her istekten sonra offset += limit; offset >= total ise dur
# Her istek: "offset 0 -> 8 books"; sonda "total: 23"
