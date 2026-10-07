from collections import defaultdict

lines = [
    "big data needs many machines",
    "many machines need a plan",
    "map then shuffle then reduce",
    "reduce needs the shuffle",
    "data moves in the shuffle",
]


def mapper(line):
    for word in line.split():
        yield word, 1


def reducer(key, values):
    return key, sum(values)


groups = defaultdict(list)
for line in lines:
    for key, value in mapper(line):
        groups[key].append(value)

counts = [reducer(k, v) for k, v in groups.items()]
counts.sort(key=lambda kv: (-kv[1], kv[0]))
for word, count in counts:
    if count >= 2:
        print(word, count)
