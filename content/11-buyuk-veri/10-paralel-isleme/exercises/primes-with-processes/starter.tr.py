from concurrent.futures import ProcessPoolExecutor


def count_primes(bounds):
    start, stop = bounds
    count = 0
    for n in range(start, stop):
        if n < 2:
            continue
        d = 2
        while d * d <= n:
            if n % d == 0:
                break
            d += 1
        else:
            count += 1
    return count


if __name__ == "__main__":
    # Parcalar, surec havuzu, toplam ve karsilastirma.
    pass
