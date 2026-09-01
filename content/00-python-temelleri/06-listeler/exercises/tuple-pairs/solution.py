point = (3, 7)
x, y = point

pairs = [("Ada", 90), ("Brian", 40), ("Grace", 75)]

names = []
for pair in pairs:
    names.append(pair[0])

best = pairs[0]
for pair in pairs:
    if pair[1] > best[1]:
        best = pair

print(point)
print(x)
print(y)
print(names)
print(best)
