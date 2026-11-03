# Ethics and Law

Most of what you learned in this path can be used in both directions.
Someone who knows how a vulnerability arises can close it, or misuse it.
What keeps security knowledge on the defensive side is not technique but
two lines: **permission** and **ethics**. This section describes those
lines and how to turn them into everyday practice.

This section is **not legal advice.** Laws differ from country to country
and change over time; in a concrete situation, consult the law itself and a
lawyer. All people, addresses and systems are made up.

## Permission: the line between a test and an attack

A security test and an attack can consist of technically the same steps.
The difference between them is a single document: the system **owner's
written permission**. Without permission, even with good intentions ("I
was only curious", "I was going to show the hole and warn them"), entering
a computer system without authorisation is a crime in most countries. In
Turkey, the provisions of the Turkish Penal Code on offences in the field
of information systems cover this; Europe and other countries have similar
laws.

There is no "light" way to look into someone else's system without
permission. "Trying out" the security of a website, a school's network or
a friend's computer also needs the owner's permission. The way to learn is
an environment you set up yourself.

## Rules of engagement

An authorised test is framed, before it starts, by written **rules of
engagement**. This document says at least the following:

| Field | Why? |
|---|---|
| Written permission | The legal basis of the test |
| Who gives permission | The system's owner or a person authorised on the owner's behalf |
| Scope | Which addresses, which systems; what is explicitly excluded |
| Time window | On which days and hours the test may run |
| Emergency contact | Who is called if something goes wrong |
| Data handling | What happens to the data seen during the test |

We can check that the document is complete with a list:

```python
REQUIRED = ["written_permission", "signed_by", "scope", "window",
            "emergency_contact", "data_handling"]
plan = {
    "written_permission": True,
    "signed_by": "Eve (owner)",
    "scope": ["10.20.0.0/24"],
    "window": ["2026-11-10", "2026-11-14"],
}
missing = [name for name in REQUIRED if not plan.get(name)]
print("missing:", missing)
print("ready" if not missing else "not ready")
```

```text
missing: ['emergency_contact', 'data_handling']
not ready
```

Two fields are missing, so the plan is not ready. A missing field is not
skipped with "it will be fine anyway": in a test with no emergency contact,
if a service stops, nobody knows whom to tell.

## Scope and time window

Permission is given not to everything but to **what is written**. Even
inside a network in scope, some machines can be explicitly excluded (such
as a live database), and the permission is valid only for certain days.
Before every action, the target is checked against these three questions:

```python
import ipaddress
from datetime import date

SCOPE = [ipaddress.ip_network("10.20.0.0/24")]
EXCLUDED = {ipaddress.ip_address("10.20.0.5")}
WINDOW = (date(2026, 11, 10), date(2026, 11, 14))


def check(target, day):
    address = ipaddress.ip_address(target)
    if not WINDOW[0] <= day <= WINDOW[1]:
        return "outside the window"
    if address in EXCLUDED:
        return "excluded"
    if not any(address in net for net in SCOPE):
        return "out of scope"
    return "in scope"


for target, day in [("10.20.0.17", date(2026, 11, 11)),
                    ("10.20.0.5", date(2026, 11, 11)),
                    ("10.30.0.8", date(2026, 11, 11)),
                    ("10.20.0.17", date(2026, 11, 20))]:
    print(target, day, check(target, day))
```

```text
10.20.0.17 2026-11-11 in scope
10.20.0.5 2026-11-11 excluded
10.30.0.8 2026-11-11 out of scope
10.20.0.17 2026-11-20 outside the window
```

The same address (`10.20.0.17`) is in scope on one day and out of it on
another. The excluded machine is not tested, even though it is inside the
network in scope. This code connects to nothing; it only compares addresses
and dates.

## Who can give permission?

The person giving permission must have **authority** over that system.
Having access to a system does not mean being able to allow it to be
tested: an employee cannot have even the server they use tested without
its owner's approval. With cloud services, the provider's own testing rules
apply as well.

```python
OWNERS = {"shop.example.org": "Eve", "db.example.org": "Eve",
          "mail.example.org": "Bob"}
permission = {"signed_by": "Bob",
              "targets": ["shop.example.org", "mail.example.org"]}
for target in permission["targets"]:
    owner = OWNERS.get(target)
    if owner == permission["signed_by"]:
        print(target, "ok")
    else:
        print(target, "needs", owner)
```

```text
shop.example.org needs Eve
mail.example.org ok
```

Bob's signature is valid for his own system, not for Eve's.

## Data seen during a test

Even in an authorised test, you can come across personal data. The ethical
rule is simple: **look at no more than needed, do not copy, do not share.**
To show that a vulnerability exists, the existence of one record is enough;
there is no need to download the whole table. Examples that go into the
report are masked (data minimisation from the Privacy and Data Protection
section):

```python
import re

finding = "Login page leaks ada@example.org and bob@example.org in an error."


def mask(match):
    user, domain = match.group(0).split("@")
    return user[0] + "***@" + domain


print(re.sub(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+", mask, finding))
```

```text
Login page leaks a***@example.org and b***@example.org in an error.
```

The report still clearly describes the vulnerability but does not say whose
email it is. When the test ends, data gathered in scope is deleted as the
agreement says.

## Professional ethics

The principles followed by people working in security rest on the same
foundation in almost every professional body:

- **Do no harm.** The test must not stop the system or corrupt data.
- **Protect confidentiality.** Do not share the secrets and data you see
  with anyone.
- **Report honestly.** Do not shrink or inflate what you found; do not
  present what you did not find as found.
- **Stay within your competence.** Do not take on work you do not know as
  if you knew it.
- **Declare conflicts of interest.** If you also work with the competitor
  of the company you are testing, say so openly.

## Summary

- What separates a test from an attack is the owner's **written
  permission**; unauthorised access is a crime in most countries.
- An authorised test starts with **rules of engagement**: permission, who
  gives it, scope, time window, emergency contact, data handling.
- Before every action, the target is checked against the **scope, the
  exclusions and the time window**.
- Only someone with **authority** over the system can give permission.
- Data seen during a test is minimised and **masked** in the report.
- This section is not legal advice.
