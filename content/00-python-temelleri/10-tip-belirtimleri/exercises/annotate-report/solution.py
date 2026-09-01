grades: dict[str, list[int]] = {"Ada": [90, 85], "Alan": [70, 95]}


def best(records: dict[str, list[int]]) -> dict[str, int]:
    result: dict[str, int] = {}
    for name in records:
        result[name] = max(records[name])
    return result


print(best(grades))
