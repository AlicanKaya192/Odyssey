def count_guesses(n, secret):
    lo, hi = 1, n
    guesses = 0
    # Every round guess the middle and count the guess.

    return guesses


worst_100 = max(count_guesses(100, s) for s in range(1, 101))
print(100, worst_100)
n = 1_000_000
print(n, max(count_guesses(n, 1), count_guesses(n, n)))
