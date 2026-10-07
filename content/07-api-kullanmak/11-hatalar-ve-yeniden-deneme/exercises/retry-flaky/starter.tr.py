import time

import requests

BASE = "http://api.odyssey.test"

# En fazla 5 deneme: "attempt 1 503"; 200 ise cik, degilse time.sleep(1)


# "report: ready", "after attempt: 3"
