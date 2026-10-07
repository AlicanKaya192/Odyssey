from stream_data import payments
from collections import defaultdict

LATENESS = 30

truth = defaultdict(int)
for event in payments(5_000):
    truth[event["ts"] // 60 * 60] += 1

open_windows = defaultdict(int)
results = {}
newest = 0
dropped = 0
for event in payments(5_000, late=True):
    start = event["ts"] // 60 * 60
    if start + 60 <= newest - LATENESS:
        dropped += 1
        continue
    open_windows[start] += 1
    newest = max(newest, event["ts"])
    for s in [s for s in open_windows if s + 60 <= newest - LATENESS]:
        results[s] = open_windows.pop(s)
for s in list(open_windows):
    results[s] = open_windows.pop(s)

short = sum(1 for s in results if results[s] != truth[s])
print(dropped)
print(short)
print(sum(results.values()) + dropped == 5_000)
