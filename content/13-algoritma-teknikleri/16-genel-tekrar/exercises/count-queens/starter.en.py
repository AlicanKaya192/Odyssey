def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()

    def place(row):
        # One solution if row == n; otherwise try every column.
        return 0

    return place(0)

for n in range(1, 9):
    print(n, count_queens(n))
