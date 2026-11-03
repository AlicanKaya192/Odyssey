def delay_after(failures, start, cap):
    if failures < start:
        return 0
    return min(2 ** (failures - start), cap)

print([delay_after(n, 3, 300) for n in range(1, 8)])
print(delay_after(20, 3, 300))
