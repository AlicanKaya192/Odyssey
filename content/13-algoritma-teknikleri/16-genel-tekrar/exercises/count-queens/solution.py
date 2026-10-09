def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()

    def place(row):
        if row == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or row - c in diag1 or row + c in diag2:
                continue
            cols.add(c)
            diag1.add(row - c)
            diag2.add(row + c)
            total += place(row + 1)
            cols.remove(c)
            diag1.remove(row - c)
            diag2.remove(row + c)
        return total

    return place(0)

for n in range(1, 9):
    print(n, count_queens(n))
