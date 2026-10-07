import json

primes = [n for n in range(2, 50) if all(n % d for d in range(2, n))]
with open("/out/primes.json", "w") as handle:
    json.dump(primes, handle)
