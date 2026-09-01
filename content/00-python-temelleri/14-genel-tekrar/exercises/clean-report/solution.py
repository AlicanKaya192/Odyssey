scores = {}
skipped = 0

with open("data.txt", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        try:
            name, value = line.split(",")
            scores[name] = int(value)
        except ValueError:
            skipped = skipped + 1


print(scores)
print(skipped)
