import json

with open("/app/primes.json") as handle:
    primes = json.load(handle)
print(len(primes), "primes, the largest is", primes[-1])
