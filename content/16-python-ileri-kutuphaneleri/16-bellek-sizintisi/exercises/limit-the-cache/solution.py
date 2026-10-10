from functools import lru_cache


@lru_cache(maxsize=256)
def price(product_id):
    return product_id * 3 + 1

for i in range(5_000):
    price(i % 1_000)
print(price.cache_info().currsize, price(7))
