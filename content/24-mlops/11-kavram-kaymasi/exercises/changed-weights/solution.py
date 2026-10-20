def changed_weights(names, old, new, limit):
    changes = []
    for name, a, b in zip(names, old, new):
        diff = round(b - a, 2)
        if abs(diff) > limit:
            changes.append([name, diff])
    return sorted(changes, key=lambda pair: -abs(pair[1]))


names = ["tenure", "fee", "calls"]
for row in changed_weights(names, [-1.25, 0.87, 1.02], [-1.31, 1.89, 0.24], 0.5):
    print(row)
print(changed_weights(names, [1, 2, 3], [1, 2, 3], 0.1))
