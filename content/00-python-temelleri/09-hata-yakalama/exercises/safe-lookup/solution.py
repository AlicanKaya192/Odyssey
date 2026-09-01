def lookup(data, key):
    try:
        return data[key]
    except (KeyError, IndexError):
        return "missing"


print(lookup({"a": 1}, "a"))
print(lookup({"a": 1}, "b"))
print(lookup([10, 20], 1))
print(lookup([10, 20], 5))
