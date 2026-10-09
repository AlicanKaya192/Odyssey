def kth_highest(scores, k):
    counts = [0] * 101
    for score in scores:
        counts[score] += 1
    seen = 0
    for score in range(100, -1, -1):
        seen += counts[score]
        if seen >= k:
            return score
    return None


data = [70, 95, 80, 95, 60]
print(kth_highest(data, 1))
print(kth_highest(data, 3))
print(kth_highest(data, 9))
