def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()
    count = 0

    def place(row):
        nonlocal count
        # Past the last row? Otherwise try every column.
        pass

    place(0)
    return count


for n in [4, 6, 8]:
    print(n, count_queens(n))
print(11, count_queens(11))
