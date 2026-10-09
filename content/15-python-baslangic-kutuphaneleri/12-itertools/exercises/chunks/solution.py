from itertools import batched


def chunks(items, n):
    return [list(piece) for piece in batched(items, n)]

print(chunks(["a", "b", "c", "d", "e"], 2))
