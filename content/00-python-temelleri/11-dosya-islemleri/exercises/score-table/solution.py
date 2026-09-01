scores = {}

with open("scores.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        name, value = line.split(",")
        scores[name] = int(value)


average = sum(scores.values()) // len(scores)

top = ""
best = 0
for name in scores:
    if scores[name] > best:
        best = scores[name]
        top = name


print(scores)
print(average)
print(top)
