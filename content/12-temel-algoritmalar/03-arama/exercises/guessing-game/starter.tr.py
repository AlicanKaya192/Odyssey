def count_guesses(n, secret):
    lo, hi = 1, n
    guesses = 0
    # Her turda ortayi tahmin et, tahmini say.

    return guesses


worst_100 = max(count_guesses(100, s) for s in range(1, 101))
print(100, worst_100)
n = 1_000_000
print(n, max(count_guesses(n, 1), count_guesses(n, n)))
