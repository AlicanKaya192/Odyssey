import operator
from functools import reduce


def product_of(values):
    return reduce(operator.mul, values, 1)

print(product_of([2, 3, 4]))
print(product_of([]))
