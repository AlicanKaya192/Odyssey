import math
import re


def count(text):
    pieces = re.findall(r"\w+|[^\w\s]", text)
    return sum(math.ceil(len(p) / 4) for p in pieces)


print(count("cat"), count("capital"), count("Hello, world!"))
