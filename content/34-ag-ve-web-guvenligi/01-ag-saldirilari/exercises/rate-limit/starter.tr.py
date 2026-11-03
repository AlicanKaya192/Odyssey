from collections import deque


def rate_limit(calls, limit, window):
    times = deque()
    result = []
    for now, src in calls:
        while times and now - times[0] >= window:
            times.popleft()
        if len(times) >= limit:
            result.append(False)
        else:
            times.append(now)
            result.append(True)
    return result

calls = [[0, "a"], [1, "a"], [2, "b"], [3, "a"],
         [4, "b"], [12, "a"]]
for (t, src), ok in zip(calls,rate_limit(calls, 2, 10)):
    print(t, src, ok)
