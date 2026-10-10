from functools import lru_cache

_prices = {}


def price(product_id):
    if product_id not in _prices:
        _prices[product_id] = product_id * 3 + 1
    return _prices[product_id]

for i in range(5_000):
    price(i % 1_000)
print(price.cache_info().currsize, price(7))
