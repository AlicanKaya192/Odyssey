import math


def count_primes(n):
    if n < 2:
        return 0
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    # Her asalin katlarini p * p'den baslayarak isaretle.
    return sum(is_prime)

print(count_primes(30))
print(count_primes(100_000))
print(count_primes(5_000_000))
