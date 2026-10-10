def report(rows):
    return {key: rows.count(key) for key in set(rows)}

rows = [i % 8_000 for i in range(300_000)]
result = report(rows)
print(len(result), result[7])
