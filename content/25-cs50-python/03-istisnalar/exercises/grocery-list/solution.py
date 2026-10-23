counts = {}
while True:
    try:
        item = input().strip().upper()
    except EOFError:
        break
    if item in counts:
        counts[item] += 1
    else:
        counts[item] = 1

for item in sorted(counts):
    print(counts[item], item)
