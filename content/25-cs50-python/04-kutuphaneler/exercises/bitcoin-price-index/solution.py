import sys

import requests

if len(sys.argv) < 2:
    sys.exit("Missing command-line argument")
try:
    n = float(sys.argv[1])
except ValueError:
    sys.exit("Command-line argument is not a number")

try:
    response = requests.get("http://api.odyssey.test/v3/assets/bitcoin")
    response.raise_for_status()
except requests.RequestException:
    sys.exit("Could not reach the API")

price = float(response.json()["data"]["priceUsd"])
amount = n * price
print(f"${amount:,.4f}")
