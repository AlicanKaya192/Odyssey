def count_queens(n):
    cols, diag1, diag2 = set(), set(), set()

    def place(row):
        # row == n ise bir cozum; degilse her sutunu dene.
        return 0

    return place(0)

for n in range(1, 9):
    print(n, count_queens(n))
