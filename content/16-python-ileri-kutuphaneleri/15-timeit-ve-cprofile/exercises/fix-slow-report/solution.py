from collections import Counter


def report(rows):
    return dict(Counter(rows))

rows = [i % 8_000 for i in range(300_000)]
result = report(rows)
print(len(result), result[7])
