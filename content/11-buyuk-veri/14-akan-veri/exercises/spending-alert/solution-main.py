from stream_data import payments
from collections import defaultdict, deque

recent = defaultdict(deque)
spent = defaultdict(float)
alerts = 0

for event in payments(20_000):
    card = event["card"]
    before = spent[card]
    recent[card].append((event["ts"], event["amount"]))
    spent[card] += event["amount"]
    while recent[card][0][0] <= event["ts"] - 120:
        old_ts, old_amount = recent[card].popleft()
        spent[card] -= old_amount
    if before <= 1000 < spent[card]:
        alerts += 1
        if alerts <= 3:
            print(event["event_id"], card, round(spent[card], 2))

print(alerts)
