from stream_data import payments

current = None
count = 0
total = 0.0

for event in payments(2_000):
    start = event["ts"] // 300 * 300
    if start != current:
        if current is not None:
            print("closed", current, count, round(total, 2))
        current, count, total = start, 0, 0.0
    count += 1
    total += event["amount"]

print("open", current, count, round(total, 2))
