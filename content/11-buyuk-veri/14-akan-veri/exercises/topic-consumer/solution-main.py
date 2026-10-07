from stream_data import payments
from minilog import Topic

topic = Topic("payments", partitions=3)

for event in payments(3_000, duplicates=True):
    topic.send(event["card"], event)
print([topic.end_offset(p) for p in range(topic.partitions)])

offsets = {0: 0, 1: 0, 2: 0}
read = 0
seen = set()
revenue = 0.0
for p in offsets:
    while offsets[p] < topic.end_offset(p):
        batch = topic.read(p, offsets[p], max_records=250)
        for offset, card, event in batch:
            read += 1
            if event["event_id"] in seen:
                continue
            seen.add(event["event_id"])
            revenue += event["amount"]
        offsets[p] = batch[-1][0] + 1

print(read, len(seen))
print(round(revenue, 2))
expected = sum(event["amount"] for event in payments(3_000))
print(round(revenue, 2) == round(expected, 2))
