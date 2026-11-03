## Steps and questions

| Step | Question to ask |
|---|---|
| Preparation | Are the plan, roles and contact list ready? Are there logs and backups? |
| Detection and analysis | Is the alert real? When did it start, what does it affect? |
| Containment | How do we stop the spread without losing traces? |
| Eradication | What is the root cause, how is it removed? |
| Recovery | Is the system clean, how do we watch it once it is back? |
| Post-incident | What did we learn, which action is owned by whom, by when? |

## Priority

| Score (impact × urgency) | Priority |
|---|---|
| 6–9 | P1: now, everyone |
| 4–5 | P2: today |
| 1–3 | P3: joins the queue |

## Common mistakes

| Mistake | Why is it bad? |
|---|---|
| Switching the machine off or wiping it at once | The traces in memory and on disk are lost |
| Talking over a channel the attacker can see (the same email) | The plan reaches the attacker |
| Removing only the symptom | The root cause stays, the incident repeats |
| Building the timeline with local times | The order of events is read wrongly |
| Skipping the post-incident review | No lesson is learned |

## Python patterns

- Priority: `"P1" if s >= 6 else "P2" if s >= 4 else "P3"`.
- Converting to UTC: `datetime.fromisoformat(s).astimezone(timezone.utc)`.
- Indicator contact: contact if `INDICATORS & set(seen)` is not empty.
- A time difference in hours: `(b - a).total_seconds() / 3600`.

## Keep in mind

- Response is planned in advance, not during the incident.
- During containment a machine is taken off the network but not switched
  off.
- `.example`, `example.org` and `example.net` are reserved for example
  domains; example data never uses a real domain.
- A post-incident review produces action items, not culprits.
