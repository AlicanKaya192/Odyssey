from collections import deque


def moving_average(values, window):
    recent = deque(maxlen=window)
    averages = []
    for value in values:
        recent.append(value)
        averages.append(round(sum(recent) / len(recent), 2))
    return averages

print(moving_average([10, 20, 30, 40, 50], 3))
print(moving_average([5, 5, 5], 5))
