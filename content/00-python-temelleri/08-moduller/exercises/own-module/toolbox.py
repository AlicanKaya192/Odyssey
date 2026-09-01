"""A small helper module that ships with this exercise.

It sits in the same folder as your code, so `import toolbox` finds it.
You do not need to change this file; read it and use what is inside.
"""

# The value added tax rate used by the helpers below.
TAX_RATE = 0.20


def with_tax(price):
    """Returns the price with tax added."""
    return price + price * TAX_RATE


def discount(price, percent):
    """Returns the price after taking the given percentage off."""
    return price - price * percent / 100
