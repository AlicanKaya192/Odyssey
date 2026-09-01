values = ["12", "7", "abc", "30", "5x"]

total = 0
skipped = 0

for value in values:
    try:
        total += int(value)
    except ValueError:
        skipped += 1

print(total)
print(skipped)
