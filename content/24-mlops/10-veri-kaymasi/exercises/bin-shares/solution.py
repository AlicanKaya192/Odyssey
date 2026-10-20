import bisect


def bin_shares(values, edges):
    counts = [0] * (len(edges) + 1)
    for value in values:
        counts[bisect.bisect_left(edges, value)] += 1
    return [round(count / len(values), 3) for count in counts]


edges = [10, 20, 30]
print(bin_shares([5, 12, 18, 25, 40], edges))
print(bin_shares([10, 20, 30, 31], edges))
