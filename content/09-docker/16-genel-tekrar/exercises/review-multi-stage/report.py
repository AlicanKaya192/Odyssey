rows = [("apples", 12), ("pears", 7), ("plums", 30)]
total = 0
for name, count in rows:
    total += count
    print(f"{name:<8}{count:>4}")
print(f"{'total':<8}{total:>4}")
