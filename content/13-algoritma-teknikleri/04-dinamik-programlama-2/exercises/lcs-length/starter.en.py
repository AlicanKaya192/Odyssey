def lcs_length(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    # On a match +1 from the diagonal, otherwise above or left.
    return dp[-1][-1]


print(lcs_length("ABCBDAB", "BDCABA"))
print(lcs_length("algorithm", "altruistic"))
x = "".join("ACGT"[(i * 7) % 4] for i in range(1500))
y = "".join("ACGT"[(i * i) % 4] for i in range(1500))
print(lcs_length(x, y))
