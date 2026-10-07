import time

import requests

BASE = "http://api.odyssey.test"

# At most 5 attempts: "attempt 1 503"; leave on 200, otherwise time.sleep(1)


# "report: ready", "after attempt: 3"
