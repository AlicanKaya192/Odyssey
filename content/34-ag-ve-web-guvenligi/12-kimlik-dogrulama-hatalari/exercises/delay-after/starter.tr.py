def delay_after(failures, start, cap):
    return 2 ** failures

print([delay_after(n, 3, 300) for n in range(1, 8)])
print(delay_after(20, 3, 300))
