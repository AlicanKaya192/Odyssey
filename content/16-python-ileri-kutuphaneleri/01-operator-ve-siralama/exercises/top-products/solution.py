import heapq
from operator import itemgetter


def top_products(products, n):
    best = heapq.nlargest(n, products, key=itemgetter("sales"))
    return [p["name"] for p in best]

products = [{"name": "pen", "sales": 120}, {"name": "ink", "sales": 45},
            {"name": "book", "sales": 300}, {"name": "clip", "sales": 120}]
print(top_products(products, 2))
