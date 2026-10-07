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
    parts = [(i * 25_000, (i + 1) * 25_000) for i in range(4)]
    with ProcessPoolExecutor(max_workers=2) as ex:
        counts = list(ex.map(count_primes, parts))
    print(counts)
    total = sum(counts)
    print(total)
    print(total == sum(map(count_primes, parts)))
