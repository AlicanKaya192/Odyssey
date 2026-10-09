from itertools import groupby


def longest_streak(results, target):
    best = 0
    for key, group in groupby(results):
        if key == target:
            best = max(best, len(list(group)))
    return best

print(longest_streak("WWLWWWLL", "W"))
print(longest_streak("WWLWWWLL", "L"))
