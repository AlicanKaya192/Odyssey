# Logging and Monitoring

In the previous sections we saw defenses: permissions, authorization
checks, secure defaults. But no defense is perfect. To be able to **notice**
when something goes wrong and to **understand what happened** afterwards,
systems need to record events. This is called **logging**, and following
the logs continuously to catch situations that need attention is called
**monitoring**.

Without logs an attack may never be noticed; even if it is, how long it
lasted and what it touched cannot be known. All the logs in this section
are fake, hand-written lines.

## A good log line

The record of a security event answers five questions:

| Question | Field | Example |
|---|---|---|
| When? | `time` | `2026-11-01T10:00:07Z` |
| Who? | `user` | `bob` |
| From where? | `source` | `203.0.113.7` |
| Did what? | `event` | `login` |
| With what result? | `result` | `fail` |

What is **not written** to the log matters just as much: passwords, session
tokens, card numbers and more personal data than needed stay out of the
log (the Secrets Management and Privacy and Data Protection sections).

## Structured logs

A free sentence such as "bob could not log in" is easy for a human to
read, but hard for a program to search for among thousands of lines. That
is why logs are written **structured**: each line is a JSON object
carrying its fields by name.

```python
import json
from collections import Counter

LINES = [
    '{"t": "10:00:01", "level": "INFO", "user": "ada", "event": "login_ok"}',
    '{"t": "10:00:07", "level": "WARNING", "user": "bob", "event": "login_fail"}',
    '{"t": "10:00:09", "level": "WARNING", "user": "bob", "event": "login_fail"}',
    '{"t": "10:01:30", "level": "ERROR", "user": "-", "event": "db_timeout"}',
]
records = [json.loads(line) for line in LINES]
print(Counter(r["level"] for r in records))
print([r["t"] for r in records if r["event"] == "login_fail"])
```

```text
Counter({'WARNING': 2, 'INFO': 1, 'ERROR': 1})
['10:00:07', '10:00:09']
```

Counting the levels and finding the failed logins took one line each,
because the fields sit by name. **Log levels** (`DEBUG`, `INFO`, `WARNING`,
`ERROR`, `CRITICAL`) say how important an event is; monitoring tools look
at the higher levels first.

## Time: every log must speak the same language

Understanding an event means putting the logs of different systems side by
side **in time order**. If the systems' clocks are in different time zones,
that order misleads:

```python
from datetime import datetime, timezone

STAMPS = ["2026-11-01T10:00:05+03:00", "2026-11-01T07:00:02+00:00"]
for stamp in STAMPS:
    utc = datetime.fromisoformat(stamp).astimezone(timezone.utc)
    print(stamp, "->", utc.strftime("%H:%M:%S"))
```

```text
2026-11-01T10:00:05+03:00 -> 07:00:05
2026-11-01T07:00:02+00:00 -> 07:00:02
```

By local time the first seems to be at `10:00` and the second at `07:00`;
converted to a common clock (UTC), the second event actually happened **3
seconds earlier**. That is why logs are written with a time zone, or
directly in UTC, and the systems' clocks are synchronised with a time
server.

## Monitoring: threshold and window

Monitoring looks for **patterns** in the logs. The simplest pattern is a
count: "five failed logins within one minute". To find it, a sliding **time
window** is kept: the new event is added and old events that fall outside
the window are dropped.

```python
from collections import deque

FAILS = [0, 5, 12, 20, 31, 44, 200, 205]
WINDOW, LIMIT = 60, 5
window = deque()
for t in FAILS:
    window.append(t)
    while window[0] <= t - WINDOW:
        window.popleft()
    if len(window) >= LIMIT:
        print("alert at", t, "with", len(window), "failures")
```

```text
alert at 31 with 5 failures
alert at 44 with 6 failures
```

Because the first six failures fit into one minute, alerts came at seconds
31 and 44. The failures at second 200 stayed alone. Choosing the window
and the threshold strikes the balance we saw in the Privilege Escalation
section: a narrow window and a high threshold miss slow attempts, a wide
window and a low threshold produce false alarms.

## The integrity of logs

An attacker may try to change the logs to remove their traces. Against
this, logs are sent to a **separate system** (they do not stay on the
machine the attacker reached) and changes are made **detectable**. One way
is a hash chain: each line's hash also includes the previous line's hash.

```python
import hashlib


def chain(entries):
    prev = "0" * 64
    hashes = []
    for entry in entries:
        prev = hashlib.sha256((prev + entry).encode()).hexdigest()
        hashes.append(prev)
    return hashes


LOG = ["login ada ok", "delete report-7", "logout ada"]
saved = chain(LOG)
tampered = ["login ada ok", "delete report-8", "logout ada"]
print([a == b for a, b in zip(saved, chain(tampered))])
```

```text
[True, False, False]
```

Only one digit changed in the second line, yet **every** hash from that
line on stopped matching. Where the change happened, and everything after
it, became visible on its own. A hash chain does not stop changes, it makes
them noticeable; the chain's last hash must be kept in a separate place.

## How long is it kept?

Logs are not kept forever: they take space, and the personal data in them
is a burden. The **retention** period is set in writing according to the
law and the organisation's needs. If it is too short, the traces of an
attack noticed late will have been deleted; if too long, unneeded data
piles up.

## Summary

- **Logging** writes events down, **monitoring** follows them and looks
  for patterns.
- A good log entry: when, who, from where, did what, with what result;
  passwords and tokens are **not written**.
- **Structured (JSON) logs** can be searched by a program; levels say how
  important an event is.
- Clocks are converted to **UTC** and synchronised; otherwise the order of
  events misleads.
- Monitoring works with a **window and a threshold**; the choice is a
  balance between false alarms and misses.
- Logs are sent to a separate system; a **hash chain** makes changes
  noticeable.
