from concurrent.futures import ThreadPoolExecutor


def check(x):
    if x < 0:
        raise ValueError(f"negative: {x}")
    return x * 10


def run_all(values):
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(check, v) for v in values]
        return [f.result() for f in futures]

print(run_all([1, -2, 3]))
print(run_all([]))
