import heapq
from operator import itemgetter


def top_products(products, n):
    # heapq.nlargest(..., key=itemgetter("sales"))
    return []

products = [{"name": "pen", "sales": 120}, {"name": "ink", "sales": 45},
            {"name": "book", "sales": 300}, {"name": "clip", "sales": 120}]
print(top_products(products, 2))
