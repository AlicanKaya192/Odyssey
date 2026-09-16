rows = [("Pencil", 3, 12.5), ("Notebook", 12, 145.0), ("Eraser", 5, 7.25)]

print(f"{'Product':<12}{'Qty':>5}{'Price':>10}")

for name, count, price in rows:
    print(f"{name:<12}{count:>5}{price:>10.2f}")
