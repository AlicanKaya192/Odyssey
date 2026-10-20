import zlib


def route(customer_id, percent):
    bucket = zlib.crc32(customer_id.encode()) % 100
    if bucket < percent:
        return "new"
    return "old"


ids = ["C06-%05d" % i for i in range(1, 1001)]
print(sum(route(i, 5) == "new" for i in ids))
print(route("C06-00001", 0), route("C06-00001", 100))
print(all(route(i, 25) == "new" for i in ids if route(i, 5) == "new"))
