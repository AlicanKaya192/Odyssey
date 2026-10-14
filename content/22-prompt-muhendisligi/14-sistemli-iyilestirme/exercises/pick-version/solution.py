def pick_version(results):
    best = results[0]
    for row in results[1:]:
        if row[1] > best[1]:
            best = row
    gap = round(best[1] - best[2], 2)
    return [best[0], best[2], gap, gap > 0.1]


RESULTS = [["v1", 0.6, 0.6], ["v2", 0.9, 0.75],
           ["v3", 1.0, 0.75]]
print(pick_version(RESULTS))
print(pick_version([["a", 0.8, 0.8], ["b", 0.8, 0.5]]))
