from datetime import date

start = date(2026, 1, 1)
end = date(2026, 3, 1)

gap = (end - start).days
label = start.isoformat()

print(gap)
print(label)
