import zlib


def route(customer_id, percent):
    # Kova hesapla, payla karsilastir.
    pass


ids = ["C06-%05d" % i for i in range(1, 1001)]
print(sum(route(i, 5) == "new" for i in ids))
print(route("C06-00001", 0), route("C06-00001", 100))
print(all(route(i, 25) == "new" for i in ids if route(i, 5) == "new"))
