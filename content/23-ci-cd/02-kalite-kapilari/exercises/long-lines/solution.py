SAMPLE = """def total(prices):
    result = 0
    for price in prices:
        result = result + price  # add every price in the list to the running total
    return result
"""


def long_lines(source, limit):
    found = []
    number = 1
    for line in source.split("\n"):
        if len(line) > limit:
            found.append(number)
        number = number + 1
    return found


print(long_lines(SAMPLE, 40))
print(long_lines(SAMPLE, 79))
print(long_lines("a\nbb\nccc", 2))
