import time

import requests

BASE = "http://api.odyssey.test"

# get_with_retry(url, attempts): <500 hemen dondur; 5xx/Timeout/ConnectionError'da
# 0.5, 1, 2... bekleyip yeniden dene; son denemeden sonra bekleme; bitince None


# "/flaky -> 200", "/books/99 -> 404", "/broken -> gave up"
