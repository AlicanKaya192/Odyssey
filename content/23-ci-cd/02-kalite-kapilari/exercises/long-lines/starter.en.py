SAMPLE = """def total(prices):
    result = 0
    for price in prices:
        result = result + price  # add every price in the list to the running total
    return result
"""


def long_lines(source, limit):
    # Count the lines; add the numbers of the long ones to the list.
    pass


print(long_lines(SAMPLE, 40))
print(long_lines(SAMPLE, 79))
print(long_lines("a\nbb\nccc", 2))
