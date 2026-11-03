def checked_add(a, b, bits):
    total = a + b
    if total >= 2 ** bits:
        return None
    return total

print(checked_add(200, 55, 8))
print(checked_add(200, 56, 8))
print(checked_add(200, 100, 8))
print(checked_add(200, 100, 16))
