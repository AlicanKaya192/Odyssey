votes = ["python", "go", "python", "rust", "go", "python"]

counts = {}
for vote in votes:
    if vote in counts:
        counts[vote] = counts[vote] + 1
    else:
        counts[vote] = 1

print(counts)
