def prefix_sums(values):
    prefix = [0]
    for x in values:
        prefix.append(prefix[-1] + x)
    return prefix


print(prefix_sums([3, 1, 4, 1, 5]))
print(prefix_sums([]))
