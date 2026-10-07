import time

import requests

BASE = "http://api.odyssey.test"

# get_with_retry(url, attempts): return at once below 500; on 5xx/Timeout/ConnectionError
# wait 0.5, 1, 2... and try again; no wait after the last attempt; None at the end


# "/flaky -> 200", "/books/99 -> 404", "/broken -> gave up"
