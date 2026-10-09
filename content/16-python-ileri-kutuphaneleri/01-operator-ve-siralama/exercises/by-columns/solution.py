from operator import itemgetter


def by_columns(rows, cols):
    return sorted(rows, key=itemgetter(*cols))

rows = [["book", 3, 12.0], ["ink", 10, 0.5], ["pen", 3, 1.5]]
for row in by_columns(rows, [1, 2]):
    print(row)
