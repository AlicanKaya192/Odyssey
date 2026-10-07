def min_gap(allowed, window_seconds):
    return round(window_seconds / allowed, 2)


def job_minutes(total_requests, allowed, window_seconds):
    seconds = total_requests * (window_seconds / allowed)
    return round(seconds / 60, 1)


jobs = [
    (500, 60, 60),
    (120, 3, 1),
    (10000, 1000, 3600),
]
for total, allowed, window in jobs:
    print(total, "requests: gap", min_gap(allowed, window), "s, at least",
          job_minutes(total, allowed, window), "min")
