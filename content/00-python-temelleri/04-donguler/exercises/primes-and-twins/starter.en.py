limit = 100

prime_count = 0
previous = 0
twin_a = 0
twin_b = 0

# Outer loop: every number from 2 to limit
#   Inner loop: is this number prime?
#   If prime: count it, compare it with the previous prime, update previous


print("Primes up to", limit, ":", prime_count)
print("Largest twin pair:", twin_a, twin_b)
