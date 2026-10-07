The ideas of streaming data and the patterns in this section on one page.

## Ideas

| Idea | Meaning |
|---|---|
| Event | A single record in the stream: id, time, data |
| State | A small summary updated along the stream |
| Event time | The moment the event happened |
| Processing time | The moment the event reaches the system |
| Watermark | The assumption "nothing older will arrive any more" |
| Idempotent | Processing an event twice is the same as once |

## Windows

| Window | How | Example question |
|---|---|---|
| Tumbling | Equal slices that do not overlap | How many payments each minute? |
| Sliding | The last N seconds, slides with each event | Did a card pay 5 times in the last 60 s? |
| Session | Closes when a gap is too long | How many pages in one visit? |

## Patterns

```python
# The start of a tumbling window
start = event["ts"] // 60 * 60

# A sliding window (per card)
times = recent[event["card"]]
times.append(event["ts"])
while times[0] <= event["ts"] - 60:
    times.popleft()

# The watermark
watermark = newest - lateness
if start + 60 <= watermark:
    ...  # too late: drop it or store it separately

# Removing copies
if event["event_id"] in seen:
    continue
seen.add(event["event_id"])
```

## Delivery guarantees

| Guarantee | The event | The cost |
|---|---|---|
| At most once | May be lost | An incomplete result |
| At least once | May arrive twice | Copies must be removed |
| Exactly once | Counted once | System support, slower |

## Kafka terms

| Term | Meaning |
|---|---|
| Producer | A program that writes records to a topic |
| Topic | The stream of one kind of event |
| Partition | A part of a topic; only appended to |
| Offset | A record's position in its partition |
| Key | Decides the partition; same key, same partition |
| Commit | A consumer saving where it is |
| Consumer group | Consumers that share the partitions |
| Retention | How long records are kept before deletion |

## Tools

| Tool | Role |
|---|---|
| Kafka, Kinesis, Pub/Sub | Transport and storage |
| Spark Structured Streaming | Streams as small batch jobs |
| Flink | Event by event, low delay |
