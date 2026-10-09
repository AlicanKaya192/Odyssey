def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


for n in [1, 2, 8, 1000, 1_000_000]:
    print(n, halving_steps(n))
