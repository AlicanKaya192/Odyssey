# Intrusion Detection (IDS)

In the Logging and Monitoring section we saw how to collect logs and
produce alerts with simple thresholds. An **Intrusion Detection System**
(IDS) is the specialised form of that idea: it examines network traffic or
system events continuously and produces an alert for anything that looks
like an attack.

This section covers the two main detection methods, how a detection system
is **measured**, and how events that look harmless one by one can mean
something together. All the data is fake: hand-written request lines,
event lists and example IP addresses reserved for documentation
(`203.0.113.0/24`, `198.51.100.0/24`).

## Where does it sit, what does it do?

| Kind | What does it look at? | Example |
|---|---|---|
| **Network-based IDS** (NIDS) | Traffic passing through the network | A detection system at a network gateway |
| **Host-based IDS** (HIDS) | A computer's own events | File changes, logins, processes |
| **IDS** | Alerts, does not stop | A notice to the security team |
| **IPS** (prevention system) | Stops what it detects | Cuts the connection |

An IPS looks stronger, but a false alarm also cuts real users' requests.
That is why a new rule is usually tried in **alert-only** mode first.

## Method 1: signatures

**Signature-based detection** looks for the distinctive traces of known
attacks. Each signature is a pattern; if a line matches the pattern, an
alert comes out:

```python
import re

RULES = {
    "path traversal": re.compile(r"\.\./"),
    "script tag": re.compile(r"<script", re.IGNORECASE),
    "sql injection": re.compile(r"'\s*or\s+1=1", re.IGNORECASE),
}
LINES = [
    "GET /index.html",
    "GET /files?name=../../etc/passwd",
    "GET /search?q=' OR 1=1 --",
    "POST /comment body=<SCRIPT>hi</SCRIPT>",
    "GET /search?q=shoes",
]
for number, line in enumerate(LINES, 1):
    for name, pattern in RULES.items():
        if pattern.search(line):
            print(number, name)
```

```text
2 path traversal
3 sql injection
4 script tag
```

The three known attack patterns were caught and the two ordinary requests
stayed quiet. A signature's strength is its **precision**: it finds what it
knows reliably and with few false alarms. Its weakness is in the same
place: it only finds what it **knows**. There is no signature for an attack
never seen before; that is why signatures are updated regularly.

## Method 2: anomalies

**Anomaly-based detection** does not try to recognise the attack; it first
learns what is **normal**, then flags anything that strays far from it.
The simplest measure is the **z-score**: how many standard deviations a
value is away from the mean.

```python
import statistics

BASELINE = [120, 130, 125, 118, 122, 127, 131, 124]
mean = statistics.mean(BASELINE)
stdev = statistics.stdev(BASELINE)
print(f"mean {mean:.1f}, stdev {stdev:.1f}")
for value in [126, 410]:
    z = (value - mean) / stdev
    print(value, f"z={z:.1f}", "ANOMALY" if abs(z) > 3 else "normal")
```

```text
mean 124.6, stdev 4.6
126 z=0.3 normal
410 z=62.1 ANOMALY
```

124.6 requests an hour are normal; 126 requests are within that range,
while 410 are 62.1 standard deviations from the mean and were flagged.
Anomaly detection can also catch attacks never seen before, but the price
is **false alarms**: a sale day or a new feature is "unusual" too. The
normal itself changes over time; that is why the baseline is recalculated
regularly.

## Measuring detection

How good is a detection system? To answer, the alerts are compared with
what really happened:

```python
ALERTS = {"e1", "e2", "e5", "e7"}
ATTACKS = {"e2", "e5", "e6"}
tp = len(ALERTS & ATTACKS)
fp = len(ALERTS - ATTACKS)
fn = len(ATTACKS - ALERTS)
print("true positives:", tp, "false positives:", fp, "missed:", fn)
print(f"precision {tp / (tp + fp):.2f}, recall {tp / (tp + fn):.2f}")
```

```text
true positives: 2 false positives: 2 missed: 1
precision 0.50, recall 0.67
```

- **Precision:** how many of the alerts are real attacks? Here
  0.50: one alert in every two is wasted.
- **Recall:** how many of the real attacks were caught? Here
  0.67: one attack in three (`e6`) was missed.

The two work against each other: lowering the threshold raises recall but
lowers precision; the alert fatigue in the Logging and Monitoring section
is the result of low precision. Because real attacks are very **rare**
among events, even a false alarm rate that looks small means hundreds of
empty alerts a day.

## Combining events

Events that look harmless alone can mean something together. Several
failed logins from the same place are normal (someone forgot their
password); but if a **successful** login follows, the password may have
been guessed:

```python
from collections import Counter

EVENTS = [
    ("10:00", "203.0.113.9", "bob", "fail"),
    ("10:01", "203.0.113.9", "bob", "fail"),
    ("10:01", "198.51.100.4", "ada", "fail"),
    ("10:02", "203.0.113.9", "bob", "fail"),
    ("10:02", "198.51.100.4", "ada", "ok"),
    ("10:03", "203.0.113.9", "bob", "fail"),
    ("10:04", "203.0.113.9", "bob", "ok"),
]
fails = Counter()
for time, ip, user, result in EVENTS:
    key = (ip, user)
    if result == "fail":
        fails[key] += 1
    elif fails[key] >= 3:
        print(time, "possible compromise:", user, "from", ip)
        print("  failures before:", fails[key])
```

```text
10:04 possible compromise: bob from 203.0.113.9
  failures before: 4
```

`ada` mistyped once and got in: normal. `bob`'s account was logged into
after four failed attempts from the same address: a strong sign the
account may have been taken over. This kind of combining is called **event
correlation**, and a good alerting system looks at such patterns more than
at single events. What to do when an alert comes is the topic of the next
section, Incident Response.

## Summary

- An **IDS** detects what looks like an attack and alerts; an **IPS**
  stops it. It is network-based (NIDS) or host-based (HIDS).
- **Signature-based detection** finds the known precisely and misses the
  new.
- **Anomaly-based detection** finds deviations from normal; it catches the
  new too but produces false alarms.
- **Precision:** how many alerts are real; **recall:** how many real ones
  were caught. The two work against each other.
- **Correlation:** patterns such as repeated failures + a success mean more
  than a single event.
