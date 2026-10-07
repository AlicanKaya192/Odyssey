Stream code can work correctly on a small example and give wrong results on a
real stream. Common mistakes.

## 1. Building windows on processing time

Putting an event into a window by the moment it arrives (`time.time()`) is
easy but wrong: a late payment is counted in the minute it arrived, not the
minute it happened. Windows are built on **event time** (`event["ts"]`).

## 2. Assuming events arrive in order

The rule "close the previous window when the first event of a new one
arrives" loses events in an out-of-order stream (6128 payments in this
section). Choose a watermark and count the late ones; if the number is high,
wait longer.

## 3. State that grows forever

```python
seen.add(event["event_id"])     # every id, forever
recent[event["card"]]           # cards that are never removed
```

If closed windows, old ids and keys that have been quiet for a long time are
not cleaned up, the state grows with the stream and memory runs out in the
end.

## 4. Counting copies

In a stream from a system with at-least-once delivery the same event may
arrive twice; in this section revenue came out 3% too high. Remove copies by
the event's id, or make the processing idempotent.

## 5. Alerting again at every event

```python
if len(times) >= 5:    # at every payment of the burst
if len(times) == 5:    # once, the moment the limit is reached
```

In this section `>= 5` gave 914 alerts and `== 5` gave 389. Alerts that
report the same thing drown the real ones.

## 6. Putting the stream in a list

`list(payments(...))` or `events.append(event)` turns the stream back into
batch processing and memory grows with the number of events (in this section,
over thirty thousand KB instead of a few KB). Keep only the summary you need.

## 7. Slow work inside the stream

Opening a file or asking something over the network at every event slows the
stream down; if events are processed more slowly than they arrive, the queue
grows and the delay keeps rising. Do slow work in batches (such as writing
once every 1000 events).

## 8. Expecting order everywhere in Kafka

Order is only guaranteed inside a partition. Events whose order matters (one
card's payments) are sent with the same key so they land in the same
partition.
