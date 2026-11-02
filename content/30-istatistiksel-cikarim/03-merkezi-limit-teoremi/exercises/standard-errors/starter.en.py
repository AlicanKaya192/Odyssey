def se_table(sigma, sizes):
    return [round(sigma / n, 3) for n in sizes]


print(se_table(6.13, [4, 16, 64]))
print(se_table(120, [100, 400]))
