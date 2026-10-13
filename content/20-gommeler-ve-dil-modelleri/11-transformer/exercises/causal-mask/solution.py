def causal_mask(n):
    return [[1 if j <= i else 0 for j in range(n)] for i in range(n)]

for row in causal_mask(4):
    print(row)
