def add_fractions(items):
    total = 0
    for item in items:
        top, bottom = item.split("/")
        total += int(top) / int(bottom)
    return str(total)

print(add_fractions(["1/3", "1/6"]))
print(add_fractions(["1/2", "1/4", "1/8"]))
