def passes_fermat(n, bases):
    for a in bases:
        if pow(a, n - 1, n) != 1:
            return False
    return True

print(passes_fermat(7, [2, 3, 5]))
print(passes_fermat(15, [4, 2]))
print(passes_fermat(561, [2, 5, 7]))
