def check_pair(e, d, n, samples):
    return e * d % n == 1

print(check_pair(17, 2753, 3233, [0, 1, 65, 3000]))
print(check_pair(17, 2754, 3233, [0, 1, 65, 3000]))
