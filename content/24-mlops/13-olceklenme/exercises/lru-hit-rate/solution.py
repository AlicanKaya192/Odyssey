from collections import OrderedDict


def hit_rate(requests, size):
    cache = OrderedDict()
    hits = 0
    for key in requests:
        if key in cache:
            hits += 1
            cache.move_to_end(key)
        else:
            cache[key] = True
            if len(cache) > size:
                cache.popitem(last=False)
    return round(hits / len(requests), 3)


requests = [1, 2, 1, 3, 1, 2, 4, 1, 2, 3]
print(hit_rate(requests, 1))
print(hit_rate(requests, 2))
print(hit_rate(requests, 3))
