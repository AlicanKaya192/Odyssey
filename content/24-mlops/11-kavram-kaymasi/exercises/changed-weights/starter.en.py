def changed_weights(names, old, new, limit):
    # Walk feature by feature with zip.
    pass


names = ["tenure", "fee", "calls"]
for row in changed_weights(names, [-1.25, 0.87, 1.02], [-1.31, 1.89, 0.24], 0.5):
    print(row)
print(changed_weights(names, [1, 2, 3], [1, 2, 3], 0.1))
