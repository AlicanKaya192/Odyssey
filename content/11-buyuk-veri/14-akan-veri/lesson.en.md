# Streaming Data

So far data has always been **sitting** somewhere: a CSV, a Parquet folder, a
table. We opened the file, read it from start to end and worked out the
result once. But a lot of data never stops: card payments, readings from the
sensors in a factory, clicks on a website. It keeps coming, day and night,
second by second, and it **has no end**.

With data like this the question is different too: "This card made five
payments in the last minute; should we stop it?" If the answer comes from a
report that runs at night, it is too late. Processing data **the moment it
arrives** is called **stream processing**.

## Batch processing and streaming

<figure class="fig">
  <div class="versus">
    <div><h4>Batch processing</h4><p>Data sits still, with an end<br>The whole file is read<br>The result comes once<br>Delay: hours</p></div>
    <div class="ok"><h4>Streaming</h4><p>Data keeps coming, no end<br>Processed event by event<br>The result keeps updating<br>Delay: seconds</p></div>
  </div>
  <figcaption>The same payments can be processed either way; the difference is when the result is needed.</figcaption>
</figure>

The two approaches are not rivals. A bank catches fraud in the stream and
produces the monthly report with batch processing. In this section we take
on four questions that belong to streams: **memory** with endless data,
**windows**, **late events**, and **the same event arriving twice**.

## A stream in Python: a generator

The exercises have a read-only `stream_data.py`. Its `payments(n)` is a card
payment stream with a fixed seed: every call gives the same payments, **one
at a time**.

```python
from stream_data import payments

for event in payments(5):
    print(event)
```

```text
{'event_id': 1, 'ts': 3, 'card': 'C116', 'amount': 182.01, 'city': 'Bursa'}
{'event_id': 2, 'ts': 4, 'card': 'C049', 'amount': 82.59, 'city': 'Istanbul'}
{'event_id': 3, 'ts': 5, 'card': 'C115', 'amount': 146.12, 'city': 'Ankara'}
{'event_id': 4, 'ts': 7, 'card': 'C153', 'amount': 155.94, 'city': 'Istanbul'}
{'event_id': 5, 'ts': 10, 'card': 'C004', 'amount': 166.69, 'city': 'Istanbul'}
```

Each payment is an **event**: an id (`event_id`), the moment it happened
(`ts`, seconds since the stream started), the card, the amount and the city.

`payments` is a **generator** (the `yield` from Section 12): it does not
build the list up front, it produces the next event whenever you ask. A
stream is exactly like that: you only have the **current** event, you cannot
go back, and you do not know when the end will come.

```python
stream = payments(1_000_000)
print(next(stream)["event_id"])
print(next(stream)["event_id"])
```

```text
1
2
```

The million-event stream was "set up", but nothing was produced yet; every
call to `next()` brings one event.

## Calculating with constant memory

If the stream has no end, you cannot keep all the events in a list. Instead,
after every event a small **summary** is updated: how many events came, what
the total is, which one was the largest. This summary is called the
**state**.

```python
count = 0
total = 0.0
largest = None
for event in payments(100_000):
    count += 1
    total += event["amount"]
    if largest is None or event["amount"] > largest["amount"]:
        largest = event
print(count, round(total, 2), round(total / count, 2))
print(largest)
```

```text
100000 12367234.15 123.67
{'event_id': 24849, 'ts': 35239, 'card': 'C063', 'amount': 3423.02, 'city': 'Istanbul'}
```

The state is just three variables: whether the stream lasts a hundred
thousand or a hundred billion events, memory stays the same. Let's measure
(`tracemalloc`, Section 1):

```python
import tracemalloc

def peak_kb(work):
    tracemalloc.start()
    work()
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return round(peak / 1024)

def streaming():
    total = 0.0
    for event in payments(100_000):
        total += event["amount"]

def as_list():
    events = list(payments(100_000))

print(peak_kb(streaming), "KB")
print(peak_kb(as_list), "KB")
```

```text
13 KB
31644 KB
```

A few KB with the stream; over thirty thousand KB when it is put in a list
first. The list grows with the number of events; the state of a stream does
not.

Not every calculation is this easy to summarise. Total, count, largest and
mean are easy; the **number of different cards** needs every card to be
remembered. There, approximate methods such as HyperLogLog from Section 9 do
the job with constant memory.

## Windows

"The total since the stream started" is rarely useful; the question is what
happened "**in the last minute**" or "**every five minutes**". Slicing a
stream by time is called a **window**. Three kinds:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Tumbling</span><span>0–60, 60–120, 120–180 … no overlap; each event in one window</span></div>
    <div class="anat-row"><span>Sliding</span><span>"the last 60 seconds" at every moment; windows overlap</span></div>
    <div class="anat-row"><span>Session</span><span>no fixed length; closes when there is a long gap between events</span></div>
  </div>
  <figcaption>The question decides the window: "every minute", "the last minute" or "one visit".</figcaption>
</figure>

### Tumbling window

Each event falls into exactly one window. The start of an event's window is
found with integer division: `ts // 60 * 60` (`ts` = 135 → 120).

```python
from collections import defaultdict

windows = defaultdict(int)
for event in payments(1_000):
    start = event["ts"] // 60 * 60
    windows[start] += 1
for start in sorted(windows)[:4]:
    print(start, windows[start])
```

```text
0 38
60 45
120 40
180 43
```

This code keeps every window until the end and prints the result at the very
end; but a stream has no end. In a stream, when a window **closes** its
result should be sent at once and forgotten. If events arrive in time order,
the first event of a new window tells you the previous one has closed:

```python
current, count = None, 0
for event in payments(300):
    start = event["ts"] // 60 * 60
    if start != current:
        if current is not None:
            print("window", current, "closed:", count, "payments")
        current, count = start, 0
    count += 1
```

```text
window 0 closed: 38 payments
window 60 closed: 45 payments
window 120 closed: 40 payments
window 180 closed: 43 payments
window 240 closed: 41 payments
window 300 closed: 42 payments
window 360 closed: 40 payments
```

The state is now only the open window. The last window (420) was not
printed: the next event that would tell us it closed never came. In a real
stream it would have.

### Sliding window: a fraud alert

"Did this card make five payments **in the last 60 seconds**?" is asked at
every new payment; the window slides along with the payments. For each card
we keep the times of its recent payments in a `deque` (a list that is quick
to add to and remove from at both ends); anything older than 60 seconds is
dropped from the left:

```python
from collections import defaultdict, deque

recent = defaultdict(deque)
alerts = 0
for event in payments(100_000):
    times = recent[event["card"]]
    times.append(event["ts"])
    while times[0] <= event["ts"] - 60:
        times.popleft()
    if len(times) == 5:
        alerts += 1
        if alerts <= 3:
            print("alert:", event["card"], "at", event["ts"])
print(alerts, "alerts")
print(len(recent), "cards in state")
```

```text
alert: C061 at 328
alert: C149 at 508
alert: C175 at 2454
389 alerts
200 cards in state
```

Two details:

- **`== 5`, not `>= 5`.** We alert once, at the fifth payment. With `>= 5`
  the sixth and seventh payments of the same burst would also raise alerts:
  914 alerts instead of 389.
- **The state is as big as the number of cards.** 200 cards, each holding at
  most a few times. If there are millions of cards the state grows too; the
  entry of a card that has not paid for a long time is removed.

### Session window

A session has no fixed length: when there is a **gap** longer than a set time
(for example 30 minutes) between a user's events, the session closes. "How
many pages were viewed in one visit" on a website is answered this way.

## Late events

So far events arrived in time order. In reality they do not: a phone is
offline for a while, the network slows down, a payment arrives a minute
later. There are two separate times:

- **Event time**: the moment the payment was made (`ts`).
- **Processing time**: the moment the event reaches the system.

`payments(n, late=True)` gives the same payments with some of them delayed:

```python
newest = -1
out_of_order = 0
worst = 0
for event in payments(100_000, late=True):
    if event["ts"] < newest:
        out_of_order += 1
        worst = max(worst, newest - event["ts"])
    newest = max(newest, event["ts"])
print(out_of_order, worst)
```

```text
8005 119
```

8005 payments arrived **after** a newer payment; the latest of them was 119
seconds behind. The rule above, "close the previous window when the first
event of a new one arrives", misses these: a payment whose window has
already closed goes into no result.

Waiting for something you know nothing about will not work either; when
should the window close? The answer of streaming systems is the
**watermark**: the assumption that "nothing older than the newest event time
seen minus `lateness` seconds will arrive any more". A window closes when the
watermark passes its end; an event arriving after that is dropped (or stored
separately).

```python
def dropped(lateness):
    open_windows = defaultdict(int)
    newest = 0
    lost = 0
    for event in payments(100_000, late=True):
        start = event["ts"] // 60 * 60
        if start + 60 <= newest - lateness:
            lost += 1
            continue
        open_windows[start] += 1
        newest = max(newest, event["ts"])
        for s in [s for s in open_windows if s + 60 <= newest - lateness]:
            del open_windows[s]
    return lost

for lateness in [0, 30, 60, 90, 120]:
    print(lateness, dropped(lateness))
```

```text
0 6128
30 4078
60 1963
90 475
120 0
```

The window's result would be sent at the `del open_windows[s]` line. The
trade-off is clear:

- **Waiting little** gives the result quickly but incomplete: with no waiting
  (0), 6128 payments were lost.
- **Waiting long** gives the full result but late: waiting 120 seconds lost no
  payments, but every minute's result arrives two minutes late.

The right value depends on the job. For fraud even a few seconds is long; for
a daily revenue report waiting an hour is no problem.

## The same event twice

When the systems that carry a stream (Kafka, coming shortly) cannot be sure an
event arrived, they send it **again**. Better than losing it, but now the
same payment may be counted twice. `payments(n, duplicates=True)` gives some
payments twice:

```python
seen = set()
received = 0
naive = 0.0
total = 0.0
for event in payments(100_000, duplicates=True):
    received += 1
    naive += event["amount"]
    if event["event_id"] in seen:
        continue
    seen.add(event["event_id"])
    total += event["amount"]
print(received, len(seen))
print(round(naive, 2), round(total, 2))
```

```text
103003 100000
12732813.33 12367234.15
```

103003 events came but 100000 of them are different. The revenue added up
without removing the copies is too high; with `event_id` used to remove them,
it is the same as the total in the constant memory part.

Here the `seen` set keeps every id, so it grows with the stream. Real
systems keep ids only for a while (as long as a copy can be late at most).

This topic is called the **delivery guarantee**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>At most once</span><span>never sent again; an event may be lost</span></div>
    <div class="anat-row"><span>At least once</span><span>sent until it is sure; an event may arrive twice</span></div>
    <div class="anat-row"><span>Exactly once</span><span>each event counted once; needs system support, costs more</span></div>
  </div>
  <figcaption>The most common choice: at-least-once delivery and removing copies by id.</figcaption>
</figure>

The most common way in practice: at-least-once delivery + making the
processing **idempotent**. If processing the same event twice gives the same
result as processing it once, a copy does no harm; removing copies by id
achieves this.

## Kafka: the log that carries the stream

The program that produces payments (a till, an app) and the one that
processes them (a fraud check, a report) are usually separate programs on
separate machines. A system is needed in between to carry events safely. The
most common one is **Apache Kafka**:

<figure class="fig">
  <div class="flow">
    <span class="node">Producers<br>till, app</span><span class="arrow">→</span>
    <span class="node acc">Topic<br>3 partitions</span><span class="arrow">→</span>
    <span class="node">Consumers<br>check, report</span>
  </div>
  <figcaption>Producers write to the topic, consumers read at their own pace; neither waits for the other.</figcaption>
</figure>

- **Topic**: the stream of one kind of event, for example `payments`.
- **Partition**: a topic is split into a few partitions so it can spread over
  many machines. Each partition is a log that is only **appended to**.
- **Offset**: a record's position in its own partition (0, 1, 2, ...).
- **Key**: records with the same key always go to the same partition, by the
  rule of Section 12's shuffle (the key's hash, the remainder by the number
  of partitions).

The read-only `minilog.py` in the exercises is a small single-process
imitation of it:

```python
from minilog import Topic

topic = Topic("payments", partitions=3)
for event in payments(6):
    p, offset = topic.send(event["card"], event["amount"])
    print(event["card"], "-> partition", p, "offset", offset)
print(topic.read(0, 0))
```

```text
C116 -> partition 0 offset 0
C049 -> partition 1 offset 0
C115 -> partition 0 offset 1
C153 -> partition 2 offset 0
C004 -> partition 2 offset 1
C152 -> partition 1 offset 1
[(0, 'C116', 182.01), (1, 'C115', 146.12)]
```

`read(partition, offset)` gives the records from that offset on as
`(offset, key, value)`. **Order is only guaranteed inside a partition**: one
card's payments are always in the same partition and in order, but the order
of two payments in different partitions is not fixed. That is why the key is
chosen as the thing whose order matters (here the card).

Kafka does **not delete** a record once it is read; records are kept for a
while (for example seven days). Every consumer remembers where it is itself,
that is, the next offset for each partition:

```python
offsets = {0: 0, 1: 0, 2: 0}
batch = topic.read(2, offsets[2], max_records=1)
print(batch)
offsets[2] = batch[-1][0] + 1
print(offsets)
```

```text
[(0, 'C153', 155.94)]
{0: 0, 1: 0, 2: 1}
```

Saving the offset is called a **commit**. If a consumer processes records and
crashes before committing, when it starts again it reads from the last
committed offset: it processes those records a **second time**. That is where
at-least-once delivery comes from, and why removing copies by id is needed.

Several consumers reading the same topic form a **consumer group**: the
topic's partitions are shared among them, and each partition is read by only
one consumer in the group. A topic with three partitions can be read in
parallel by at most three consumers; the number of partitions is the upper
limit of the parallelism.

## Real tools

| Tool | What it does |
|---|---|
| Apache Kafka | Carries and stores events (topic, partition, offset) |
| Spark Structured Streaming | Processes a stream as a series of small batch jobs |
| Apache Flink | Processes events one by one, with low delay |
| Cloud services | Kinesis (AWS), Pub/Sub (Google): managed transport |

Everything we built by hand in this section has a counterpart in these tools.
In real Spark (we are not running it here) a one-minute window and a
90-second watermark are written like this:

```python
from pyspark.sql.functions import window

counts = (stream.withWatermark("event_time", "90 seconds")
                .groupBy(window("event_time", "1 minute"))
                .count())
```

The ideas are the same: event time, window, watermark, state. The tool
changes; the questions do not.

## Summary

- Streaming data is endless and is processed as it arrives. In Python a
  stream can be thought of as a generator: you only have the current event.
- Not all events are kept; a small **state** is updated. In this example, a
  few KB with the stream and over thirty thousand KB with a list.
- **Windows**: tumbling (each event in one window), sliding (the last N
  seconds), session (closed by a gap). When a window closes its result is
  sent and its state let go.
- **Event time** differs from processing time; events arrive late and out of
  order. The **watermark** says how long to wait: waiting little gives an
  incomplete result, waiting long a late one.
- Transport systems may send an event **twice**; removing copies by id makes
  processing idempotent.
- **Kafka**: topic, partition, offset, commit, consumer group. Order is only
  guaranteed inside a partition.
