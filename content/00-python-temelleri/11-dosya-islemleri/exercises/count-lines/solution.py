with open("report.txt", encoding="utf-8") as file:
    lines = file.read().splitlines()

total = len(lines)
filled = 0

for line in lines:
    if line.strip():
        filled = filled + 1


print(total)
print(filled)
