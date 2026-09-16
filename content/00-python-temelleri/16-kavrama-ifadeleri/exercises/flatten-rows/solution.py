rows = [[3, -1, 4], [0, 5], [-2, 8, 1]]

flat = [value for row in rows for value in row]
positives = [value for row in rows for value in row if value > 0]
total = sum(value for row in rows for value in row)

print(flat)
print(positives)
print(total)
