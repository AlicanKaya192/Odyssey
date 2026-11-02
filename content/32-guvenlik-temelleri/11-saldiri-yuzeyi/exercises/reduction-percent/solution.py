def reduction_percent(before, after):
    if before == 0:
        return 0.0
    return round((before - after) / before * 100, 1)

print(reduction_percent(16, 13))
print(reduction_percent(10, 10))
print(reduction_percent(0, 0))
print(reduction_percent(8, 2))
