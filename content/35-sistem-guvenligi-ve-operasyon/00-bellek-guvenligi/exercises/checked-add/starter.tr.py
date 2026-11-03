def checked_add(a, b, bits):
    # basa sarmak yerine sigiyor mu bak
    return (a + b) % (2 ** bits)

print(checked_add(200, 55, 8))
print(checked_add(200, 56, 8))
print(checked_add(200, 100, 8))
print(checked_add(200, 100, 16))
