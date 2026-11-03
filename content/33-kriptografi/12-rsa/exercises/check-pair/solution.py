def check_pair(e, d, n, samples):
    for m in samples:
        if pow(pow(m, e, n), d, n) != m:
            return False
    return True

print(check_pair(17, 2753, 3233, [0, 1, 65, 3000]))
print(check_pair(17, 2754, 3233, [0, 1, 65, 3000]))
