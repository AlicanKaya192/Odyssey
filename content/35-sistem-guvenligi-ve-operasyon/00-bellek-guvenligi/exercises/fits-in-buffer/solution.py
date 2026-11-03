def fits(buf_size, offset, length):
    if offset < 0 or length < 0:
        return False
    return offset + length <= buf_size

print(fits(8, 0, 5))
print(fits(8, 0, 12))
print(fits(8, 6, 3))
print(fits(8, -1, 2))
