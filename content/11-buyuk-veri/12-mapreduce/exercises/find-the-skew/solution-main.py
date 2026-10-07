import zlib
from orders_data import make_orders


def partition(key, reducers):
    return zlib.crc32(key.encode()) % reducers


orders = make_orders(200_000)

machine = orders["city"].map(lambda city: partition(city, 3))
counts = machine.value_counts().sort_index()
print(counts.tolist())

shares = (counts / counts.sum() * 100).round(1)
print(shares.tolist())

print(round(counts.max() / counts.min(), 1))
