limit = 100

prime_count = 0
previous = 0
twin_a = 0
twin_b = 0

for number in range(2, limit + 1):
    is_prime = True
    for divisor in range(2, number):
        if number % divisor == 0:
            is_prime = False
            break
    if is_prime:
        prime_count = prime_count + 1
        if number - previous == 2:
            twin_a = previous
            twin_b = number
        previous = number

print("Primes up to", limit, ":", prime_count)
print("Largest twin pair:", twin_a, twin_b)
