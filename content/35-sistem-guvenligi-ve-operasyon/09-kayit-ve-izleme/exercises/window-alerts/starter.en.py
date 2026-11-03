from collections import deque


def window_alerts(times, window, limit):
    alerts = []
    recent = deque()
    for t in times:
        recent.append(t)
        # drop the ones outside the window
    return alerts

FAILS = [0, 5, 12, 20, 31, 44, 200, 205, 210, 215, 220]
print(window_alerts(FAILS, 60, 5))
print(window_alerts(FAILS, 10, 3))
