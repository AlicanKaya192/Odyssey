import doctest


def initials(name):
    """Return the initials of a name, like A.L.

    >>> initials("ada lovelace")
    'A.L.'
    >>> initials("guido")
    'G.'
    >>> initials("")
    ''
    """
    return "".join(part[0].upper() + "." for part in name.split())


print(doctest.testmod())
