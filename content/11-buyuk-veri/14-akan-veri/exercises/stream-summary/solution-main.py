from stream_data import payments

count = 0
total = 0.0
big = 0
largest = None
for event in payments(50_000):
    count += 1
    total += event["amount"]
    if event["amount"] > 1000:
        big += 1
    if largest is None or event["amount"] > largest["amount"]:
        largest = event

print(count)
print(round(total, 2))
print(round(total / count, 2))
print(big)
print(largest["event_id"], largest["amount"])
