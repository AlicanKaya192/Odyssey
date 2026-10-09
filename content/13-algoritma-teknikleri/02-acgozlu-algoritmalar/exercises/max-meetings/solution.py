def max_meetings(meetings):
    count = 0
    last_end = float("-inf")
    for start, end in sorted(meetings, key=lambda m: m[1]):
        if start >= last_end:
            count += 1
            last_end = end
    return count


print(max_meetings([[9, 17], [10, 11], [11, 12], [12, 13]]))
print(max_meetings([[1, 5], [4, 7], [6, 10]]))
big = [((i * 7919) % 1_000_000, (i * 7919) % 1_000_000 + (i * 104729) % 500 + 1) for i in range(200_000)]
print(max_meetings(big))
