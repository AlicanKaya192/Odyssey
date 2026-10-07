"""Practice data: a live stream of card payments.

payments(n) yields the same n payments every time (fixed seed), one at a
time, like a live feed. Each payment is a dict:

    {"event_id": 1, "ts": 2, "card": "C017", "amount": 129.5, "city": "Ankara"}

ts is the event time: seconds since the stream started.

late=True: some payments arrive late, so they come out of time order (a
phone was offline, the network was slow). The payments are the same; only
the order they arrive in changes.

duplicates=True: some payments are delivered twice, as a messaging system
can do. The copy has the same event_id.

Read only: you import it, you do not change it.
"""
import heapq
import random

CITIES = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"]
CITY_W = [45, 20, 15, 10, 10]


def payments(n, seed=11, late=False, duplicates=False):
    """Yields n payments one by one, in the order they arrive."""
    rng = random.Random(seed)
    delay_rng = random.Random(seed + 1)
    copy_rng = random.Random(seed + 2)
    pending = []
    order = 0
    ts = 0
    burst_card, burst_left = None, 0
    for event_id in range(1, n + 1):
        if burst_left:
            card = burst_card
            burst_left -= 1
            ts += rng.randint(0, 4)
        else:
            card = "C%03d" % rng.randint(1, 200)
            ts += rng.choice([0, 1, 1, 2, 3])
            if rng.random() < 0.004:
                burst_card, burst_left = card, 5
        event = {
            "event_id": event_id,
            "ts": ts,
            "card": card,
            "amount": round(rng.lognormvariate(4.5, 0.8), 2),
            "city": rng.choices(CITIES, CITY_W)[0],
        }
        arrival = ts
        if late and delay_rng.random() < 0.08:
            arrival += delay_rng.randint(5, 120)
        heapq.heappush(pending, (arrival, order, event))
        order += 1
        if duplicates and copy_rng.random() < 0.03:
            heapq.heappush(pending, (arrival + copy_rng.randint(1, 30), order, dict(event)))
            order += 1
        while pending and pending[0][0] <= ts:
            yield heapq.heappop(pending)[2]
    while pending:
        yield heapq.heappop(pending)[2]
