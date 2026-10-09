def last[T](items: list[T]) -> T | None:
    if not items:
        return None
    return items[-1]

print(last([3, 1, 2]), last(["a"]), last([]))
