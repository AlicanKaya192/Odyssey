from collections import defaultdict

lines = [
    "big data needs many machines",
    "many machines need a plan",
    "map then shuffle then reduce",
    "reduce needs the shuffle",
    "data moves in the shuffle",
]


def mapper(line):
    # (word, 1) for every word.
    pass


def reducer(key, values):
    # (word, total).
    pass


# Shuffle, reduce and the words that appear at least twice.
