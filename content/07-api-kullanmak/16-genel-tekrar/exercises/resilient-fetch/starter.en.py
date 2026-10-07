import time

import requests

BASE = "http://api.odyssey.test"

# get(path): wait Retry-After on 429, 1 s on 5xx; at most 5 attempts


# "/flaky 200", then "/limited 200" x5
