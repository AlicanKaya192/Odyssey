from concurrent.futures import ThreadPoolExecutor


def check(x):
    if x < 0:
        raise ValueError(f"negative: {x}")
    return x * 10


def run_all(values):
    results = []
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(check, v) for v in values]
        for future in futures:
            try:
                results.append(future.result())
            except ValueError:
                results.append("error")
    return results

print(run_all([1, -2, 3]))
print(run_all([]))
