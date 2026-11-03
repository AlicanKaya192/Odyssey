# Incident Response

The Intrusion Detection section ended with an alert: `bob`'s account was
logged into after four failed attempts. What happens now? When an alert
turns out to be a real **security incident**, everything done about it is
called **incident response**.

During an incident everyone is under stress; trying to make decisions at
that moment leads to mistakes. That is why response is planned **in
advance**: who does what, who is told, and in which order things proceed
are written down. This section covers the steps of that plan and the small
tools used in each step, with fake incident data.

## The steps of the response

<figure class="fig"><div class="flow">
  <span class="node">Preparation</span><span class="arrow">→</span>
  <span class="node acc">Detection and analysis</span><span class="arrow">→</span>
  <span class="node acc">Containment, eradication, recovery</span><span class="arrow">→</span>
  <span class="node ok">Post-incident</span>
</div><figcaption>The four steps of a common framework; the last step leads back to preparation.</figcaption></figure>

| Step | What is done? |
|---|---|
| **Preparation** | A plan, roles, a contact list, response guides, logs and backups ready |
| **Detection and analysis** | Is the alert real? What happened, when did it start, what does it affect? Set a priority |
| **Containment** | Stop the damage spreading: take a machine off the network, lock an account |
| **Eradication** | Remove the root cause: close the vulnerability, reset compromised passwords |
| **Recovery** | Bring systems back in a clean state, watch them closely |
| **Post-incident** | What did we learn? Which measure, owned by whom, by when? |

## Prioritisation

Several incidents may happen at once; they cannot all be handled at the
same speed. Priority is set by two questions: **impact** (how much damage
is it doing?) and **urgency** (how fast is it growing?). A simple method is
scoring both from 1 to 3 and multiplying:

```python
INCIDENTS = [
    ("payment service down", 3, 3),
    ("phishing email reported", 1, 2),
    ("admin login from new country", 3, 2),
    ("laptop lost, disk encrypted", 2, 2),
    ("old test server scan alert", 1, 1),
]
for name, impact, urgency in INCIDENTS:
    score = impact * urgency
    level = "P1" if score >= 6 else "P2" if score >= 4 else "P3"
    print(level, score, name)
```

```text
P1 9 payment service down
P3 2 phishing email reported
P1 6 admin login from new country
P2 4 laptop lost, disk encrypted
P3 1 old test server scan alert
```

The payment service being down and the admin account logging in from an
unusual place came out on top. The lost laptop stayed at medium priority
because its disk was encrypted: encryption is a measure taken in advance
that shrinks the impact.

## Analysis: the timeline

The answer to "what happened?" is a **timeline**: the events in different
systems' logs are put into a single order. As we saw in the Logging and
Monitoring section, every time is first converted to UTC for this:

```python
from datetime import datetime, timezone

SOURCES = {
    "vpn": [("2026-11-01T02:14:00+00:00", "login bob from 203.0.113.9")],
    "web": [("2026-11-01T05:16:30+03:00", "admin page opened by bob")],
    "db": [("2026-11-01T02:20:05+00:00", "customers table exported"),
           ("2026-11-01T02:15:10+00:00", "new db user created")],
}
events = []
for source, items in SOURCES.items():
    for stamp, text in items:
        when = datetime.fromisoformat(stamp).astimezone(timezone.utc)
        events.append((when, source, text))
for when, source, text in sorted(events):
    print(when.strftime("%H:%M:%S"), f"{source:<4}", text)
```

```text
02:14:00 vpn  login bob from 203.0.113.9
02:15:10 db   new db user created
02:16:30 web  admin page opened by bob
02:20:05 db   customers table exported
```

Four events from three sources became a single story: a login over the
remote connection, a new database user a minute later, then the admin page
and finally the table being exported. The web server's log showed `05:16`
in local time; without converting to UTC it would have fallen to the end
and the story would have been read wrongly.

## Containment: whom to isolate?

The aim of containment is to stop the damage **spreading** while the
investigation continues. The **indicators of compromise** (IOC) found in
the analysis, such as a suspicious domain or address, are searched for in
other machines' logs; machines that touched an indicator are taken off the
network:

```python
INDICATORS = {"update-check.example", "203.0.113.66"}
HOSTS = {
    "pc-ada": ["mail.example.org", "intranet.local"],
    "pc-bob": ["update-check.example", "intranet.local"],
    "srv-db": ["203.0.113.66"],
    "srv-web": ["cdn.example.net"],
}
to_isolate = sorted(h for h, seen in HOSTS.items() if INDICATORS & set(seen))
print(to_isolate)
```

```text
['pc-bob', 'srv-db']
```

Two of the four machines touched one of the indicators. The containment
decision is a balance: an isolated server does no work (a loss of
availability), a server left connected may spread the damage. Another
important rule: when isolating, the machine is **not switched off** or
wiped; the traces on it are the material for the examination we will see
in the Digital Forensics Basics section.

## Measuring: how long did it take?

How well the response went is measured with durations. The two durations
we mentioned in the Logging and Monitoring section:

- **Time to detect:** from the incident starting to it being noticed.
- **Time to respond:** from it being noticed to it being closed.

```python
from datetime import datetime

INCIDENTS = [
    ("2026-10-03T08:00", "2026-10-03T11:30", "2026-10-03T15:00"),
    ("2026-10-12T22:10", "2026-10-13T06:40", "2026-10-13T09:10"),
    ("2026-10-25T13:00", "2026-10-25T13:20", "2026-10-25T14:50"),
]


def hours(a, b):
    delta = datetime.fromisoformat(b) - datetime.fromisoformat(a)
    return delta.total_seconds() / 3600


detect = [round(hours(start, found), 1) for start, found, closed in INCIDENTS]
respond = [round(hours(found, closed), 1) for start, found, closed in INCIDENTS]
print("detect:", detect, "mean", round(sum(detect) / len(detect), 1))
print("respond:", respond, "mean", round(sum(respond) / len(respond), 1))
```

```text
detect: [3.5, 8.5, 0.3] mean 4.1
respond: [3.5, 2.5, 1.5] mean 2.5
```

The mean time to detect is 4.1 hours, but a single incident (the
second one, which started at night) pulls the mean up: monitoring on the
night shift was weak. That is exactly the value of measuring: the numbers
show what to fix in the post-incident meeting.

## Post-incident: lessons, not culprits

Every incident closes with a **post-incident review**. The aim is not to
find someone to blame but to make sure the same incident does not happen
again: since people will make mistakes, the question is how the system
can tolerate that mistake. The meeting's output is concrete **action
items**: each has an owner and a due date and is tracked until closed.

## Summary

- **Incident response** is planned in advance: roles, contacts, guides.
- The steps: preparation; detection and analysis; containment,
  eradication, recovery; post-incident.
- **Prioritisation** is done with impact and urgency.
- A **timeline** puts events from different sources into a single order
  in UTC.
- **Containment** isolates machines that touched indicators of
  compromise; the machine is not switched off, the traces are kept.
- **Time to detect and time to respond** are measured; a post-incident
  review produces action items, not culprits.
