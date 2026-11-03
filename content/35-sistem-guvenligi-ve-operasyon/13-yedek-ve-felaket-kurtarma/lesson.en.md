# Backup and Disaster Recovery

In the What Is Security? The CIA Triad section we saw that one of the three
legs of security is **availability**: data and systems must be usable when
needed. A failed disk, a table deleted by mistake, a server encrypted by
ransomware or a fire affecting a building; the last defense against all of
them is the same: a **backup** and the ability to restore it.

This section covers the rules of a good backup, the questions "how much
data can we lose, how quickly can we come back", and how we know a backup
really works. All backups, dates and files are fake.

## The 3-2-1 rule

A common starting rule: keep at least **3** copies of the data, on at
least **2** different media, with at least **1** of them in another place
(outside the building):

```python
COPIES = [
    {"name": "live", "media": "ssd", "offsite": False},
    {"name": "nas", "media": "hdd", "offsite": False},
    {"name": "cloud", "media": "object-storage", "offsite": True},
]
media = {c["media"] for c in COPIES}
offsite = sum(c["offsite"] for c in COPIES)
print("copies:", len(COPIES), "ok" if len(COPIES) >= 3 else "too few")
print("media:", len(media), "ok" if len(media) >= 2 else "too few")
print("offsite:", offsite, "ok" if offsite >= 1 else "missing")
```

```text
copies: 3 ok
media: 3 ok
offsite: 1 ok
```

Three copies, three different media, one outside: the rule holds.
Different media stop one kind of failure (disks from the same batch failing
at once) taking every copy; the copy outside protects against an event
that affects the whole building, such as fire or theft.

**Ransomware** added a condition to this rule: at least one backup must be
**offline** or **immutable**. A backup reachable over the network can also
be encrypted or deleted by the attacker who encrypts the system.

## RPO: how much data can we lose?

The **RPO** (Recovery Point Objective) is the longest data loss acceptable
in a disaster. In the worst case, the data lost equals the longest **gap**
between two backups:

```python
from datetime import datetime

BACKUPS = [
    "2026-11-01T00:00",
    "2026-11-01T06:00",
    "2026-11-01T12:00",
    "2026-11-02T00:00",
]
times = [datetime.fromisoformat(t) for t in BACKUPS]
gaps = [(b - a).total_seconds() / 3600 for a, b in zip(times, times[1:])]
print("gaps (hours):", gaps)
print("worst-case data loss:", max(gaps), "hours")
print("meets RPO of 8 hours:", max(gaps) <= 8)
```

```text
gaps (hours): [6.0, 6.0, 12.0]
worst-case data loss: 12.0 hours
meets RPO of 8 hours: False
```

During the day a backup is taken every six hours, but from noon to
midnight there is a 12-hour gap. If the target is 8 hours this
schedule misses it: a disaster in that window would lose half a day of
data.

## RTO: how quickly do we come back?

The **RTO** (Recovery Time Objective) is the latest time by which the
system must work again after a disaster. The restore time depends on the
size of the data and the restore speed:

```python
size_gb = 900
speed_gb_per_hour = 150
setup_hours = 1.5
restore_hours = setup_hours + size_gb / speed_gb_per_hour
print("estimated restore:", restore_hours, "hours")
print("meets RTO of 6 hours:", restore_hours <= 6)
```

```text
estimated restore: 7.5 hours
meets RTO of 6 hours: False
```

The data itself comes back in 6 hours, but with the
preparation added (finding hardware, setting up the system) it makes
7.5 hours: the 6-hour target is missed. RPO and RTO targets
are set together with the business; a shorter target means a more
expensive backup setup.

## An untested backup is not a backup

The only way to know a backup really works is to **try restoring it**. The
restored files are compared with the originals:

```python
import hashlib


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


ORIGINAL = {
    "orders.csv": "1,ada,30\n2,bob,45\n",
    "users.csv": "ada\nbob\n",
    "keys.txt": "k1\n",
}
RESTORED = {
    "orders.csv": "1,ada,30\n2,bob,45\n",
    "users.csv": "ada\n",
}
for name in sorted(ORIGINAL):
    if name not in RESTORED:
        print(name, "missing")
    elif digest(RESTORED[name]) != digest(ORIGINAL[name]):
        print(name, "different")
    else:
        print(name, "ok")
```

```text
keys.txt missing
orders.csv ok
users.csv different
```

Only one of the three files came back intact: one is missing, one is
partial. Without this test the problem would have come out during a real
disaster, at the moment the backup is needed most. That is why restore
tests are done regularly and on a schedule.

## How long is it kept?

Keeping every backup forever is both expensive and unnecessary. A common
scheme is **grandfather-father-son**: daily backups of the last days,
weekly backups of the last weeks and monthly backups of the months are
kept:

```python
from datetime import date, timedelta

TODAY = date(2026, 11, 1)
backups = [TODAY - timedelta(days=i) for i in range(60)]
daily = {d for d in backups if (TODAY - d).days < 7}
weekly = {d for d in backups if d.weekday() == 6 and (TODAY - d).days < 28}
monthly = {d for d in backups if d.day == 1}
keep = daily | weekly | monthly
print(len(backups), "backups,", len(keep), "kept")
print(sorted(d.isoformat() for d in keep - daily))
```

```text
60 backups, 11 kept
['2026-10-01', '2026-10-11', '2026-10-18', '2026-10-25']
```

Of 60 daily backups, 11 remain: every day of the last
week, older Sundays and the first days of months. If ransomware or a silent
corruption is noticed weeks later, an old but clean backup is still there.

## The disaster recovery plan

A backup is one part; the **disaster recovery plan** describes the whole:
which systems come back first, who does what, where the backups are, which
passwords and documents are needed (and where they are found during a
disaster). Like the backup, the plan is tested with regular **drills**.

## Summary

- **3-2-1:** three copies, two different media, one outside; at least one
  offline or immutable.
- **RPO:** the acceptable data loss; the worst case is the longest gap
  between backups.
- **RTO:** the acceptable downtime; restore time is calculated with the
  preparation included.
- **An untested backup is not a backup:** restores are tried regularly and
  compared with the original.
- **Retention:** a scheme such as grandfather-father-son keeps old but clean
  backups too.
- The **disaster recovery plan** describes the whole and is tested with
  drills.
