import time

import requests

BASE = "http://api.odyssey.test"

# get(path): 429'da Retry-After, 5xx'te 1 sn bekle; en fazla 5 deneme


# "/flaky 200", sonra "/limited 200" x5
