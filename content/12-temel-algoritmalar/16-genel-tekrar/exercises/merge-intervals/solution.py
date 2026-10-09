def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals, key=lambda iv: iv[0]):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


print(merge_intervals([[8, 10], [1, 3], [2, 6], [15, 18]]))
print(merge_intervals([[1, 4], [4, 5]]))
print(merge_intervals([]))
