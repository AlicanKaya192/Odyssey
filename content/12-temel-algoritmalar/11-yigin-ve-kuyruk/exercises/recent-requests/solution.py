from collections import deque


def recent_counts(times, window):
    queue = deque()
    counts = []
    for t in times:
        queue.append(t)
        while queue[0] <= t - window:
            queue.popleft()
        counts.append(len(queue))
    return counts


print(recent_counts([1, 2, 5, 12, 13], 10))
print(recent_counts([], 10))
