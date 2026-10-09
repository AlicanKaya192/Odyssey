def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()
    count = 0

    def place(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            if col in cols or row - col in diag1 or row + col in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            place(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    place(0)
    return count


for n in [4, 6, 8]:
    print(n, count_queens(n))
print(11, count_queens(11))
