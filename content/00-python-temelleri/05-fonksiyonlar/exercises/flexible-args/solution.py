def total(*numbers):
    result = 0
    for number in numbers:
        result = result + number
    return result


def describe(label, **details):
    parts = []
    for key in details:
        parts.append(key + "=" + str(details[key]))
    if not parts:
        return label + ":"
    return label + ": " + ", ".join(parts)


print(total(1, 2, 3))
print(total())
print(describe("report", name="Ada", city="London"))
print(describe("empty"))
