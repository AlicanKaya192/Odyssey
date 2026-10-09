def count_guesses(n, secret):
    lo, hi = 1, n
    guesses = 0
    while lo <= hi:
        guess = (lo + hi) // 2
        guesses += 1
        if guess == secret:
            return guesses
        elif guess < secret:
            lo = guess + 1
        else:
            hi = guess - 1
    return guesses


worst_100 = max(count_guesses(100, s) for s in range(1, 101))
print(100, worst_100)
n = 1_000_000
print(n, max(count_guesses(n, 1), count_guesses(n, n)))
