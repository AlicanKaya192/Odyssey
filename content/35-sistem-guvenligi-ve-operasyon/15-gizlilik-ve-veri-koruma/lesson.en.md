# Privacy and Data Protection (KVKK, GDPR)

Security protects data from **unauthorised** people. **Privacy** looks one
step further: at how data is used even in **authorised** hands. A company
may store its customers' data with flawless security, but if it uses that
data for something the customer never agreed to, it has breached their
privacy.

The protection of personal data is regulated by law in many countries. In
Turkey **KVKK** (the Personal Data Protection Law) and in the European
Union the **GDPR** (General Data Protection Regulation) are the main rules
in this area. Both rest on the same basic ideas. This section covers those
ideas and ways of turning them into code; it is not legal advice. All
people and records are made up.

## What is personal data?

**Personal data** is any information about an identified or
**identifiable** natural person: a name, an email, a phone number, an
address, a device id, even an age and a postcode that point to a person
when combined with other information. Some data counts as **special
category** (sensitive) and is protected more strictly: health, biometric
and genetic data, religion, political opinion and the like.

| Role | Who? |
|---|---|
| **Data subject** | The person whose data is processed |
| **Controller** | Whoever decides why and how the data is processed |
| **Processor** | Whoever processes the data on the controller's behalf (e.g. a cloud service) |

## Basic principles

| Principle | In short |
|---|---|
| Lawfulness and transparency | Process with a legal basis and explain it clearly to the person |
| Purpose limitation | Do not use data collected for one purpose for another |
| Data minimisation | Collect only as much as the purpose needs |
| Accuracy | Keep data correct and up to date |
| Storage limitation | Do not keep it longer than needed |
| Security | Protect the data with suitable technical and organisational measures |

Most of these principles can turn directly into code.

## Data minimisation

Data that is not collected cannot leak. Every field of a form goes through
the question "is this really needed for this purpose?":

```python
FORM = {
    "name": "Ada",
    "email": "ada@example.org",
    "phone": "555-0100",
    "birth_date": "1990-05-01",
    "favourite_colour": "green",
}
NEEDED = {"newsletter": {"email"}, "delivery": {"name", "phone", "email"}}
for purpose, fields in NEEDED.items():
    kept = sorted(k for k in FORM if k in fields)
    dropped = sorted(set(FORM) - fields)
    print(purpose, "keeps", kept)
    print("  drops", dropped)
```

```text
newsletter keeps ['email']
  drops ['birth_date', 'favourite_colour', 'name', 'phone']
delivery keeps ['email', 'name', 'phone']
  drops ['birth_date', 'favourite_colour']
```

The newsletter needs only the email; delivery needs the name, phone and
email. The birth date and favourite colour are needed for no purpose: they
should not be collected. Data minimisation is both a legal principle and
the cheapest security measure.

## Pseudonyms: a keyed hash

For analysis, what may be needed is not who a person is but being able to
join the same person's records. **Pseudonymisation** replaces a direct
identifier (such as an email) with another value. A plain hash is not
enough for this: it can be reversed by hashing possible emails one by one
and comparing. That is why a **secret-keyed** hash (HMAC, the Message
Authentication: HMAC section) is used:

```python
import hashlib
import hmac

KEY = b"kept-in-the-vault"


def pseudonym(value):
    return hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()[:12]


print(pseudonym("ada@example.org"))
print(pseudonym("ada@example.org") == pseudonym("ada@example.org"))
print(pseudonym("bob@example.org"))
```

```text
1a790762043a
True
586be60649d3
```

The same email always gives the same pseudonym, so records can be joined;
different people get different pseudonyms. Someone without the key cannot
go back from the pseudonym to the email. But because whoever holds the key
can, pseudonymised data is **still personal data**; it only reduces the
risk. Data that can never again identify anyone, with any additional
information, is called **anonymous**, and achieving it is harder than it
looks.

## Data thought to be anonymous: k-anonymity

Deleting names does not make data anonymous. **Indirect identifiers** such
as age and postcode can point to a single person when combined.
**k-anonymity** requires every group with the same indirect identifiers to
contain at least **k** people. Let us generalise ages to ten-year ranges
and postcodes to their first three digits, and measure:

```python
from collections import Counter

ROWS = [
    {"age": 34, "zip": "34710", "illness": "flu"},
    {"age": 36, "zip": "34712", "illness": "asthma"},
    {"age": 35, "zip": "34718", "illness": "flu"},
    {"age": 52, "zip": "06420", "illness": "diabetes"},
    {"age": 58, "zip": "06425", "illness": "flu"},
    {"age": 41, "zip": "35210", "illness": "asthma"},
]


def generalise(row):
    decade = row["age"] // 10 * 10
    return (f"{decade}-{decade + 9}", row["zip"][:3] + "**")


groups = Counter(generalise(r) for r in ROWS)
for key, size in groups.items():
    print(key, size)
print("k =", min(groups.values()))
```

```text
('30-39', '347**') 3
('50-59', '064**') 2
('40-49', '352**') 1
k = 1
```

Two groups contain more than one person, but a single person aged `40-49`
living in area `352**` is left: k = 1. Someone who knows this person
can learn their illness even though the name was deleted. Because health
data is special category, this is a serious breach. The fix is more
generalisation or leaving small groups out of the release.

## Storage limitation

Every piece of data has a purpose, and every purpose a retention period.
Data whose period is over is deleted or anonymised. The periods below are
only examples, not legal periods:

```python
from datetime import date

TODAY = date(2026, 11, 1)
RETENTION = {"marketing": 365, "invoice": 3650, "support": 730}
RECORDS = [
    ("r1", "marketing", date(2025, 6, 1)),
    ("r2", "invoice", date(2019, 2, 1)),
    ("r3", "support", date(2025, 1, 10)),
    ("r4", "marketing", date(2026, 3, 3)),
]
for rid, purpose, created in RECORDS:
    age = (TODAY - created).days
    print(rid, purpose, age, "delete" if age > RETENTION[purpose] else "keep")
```

```text
r1 marketing 518 delete
r2 invoice 2830 keep
r3 support 660 keep
r4 marketing 243 keep
```

Two records of the same kind got different results because their ages
differ. A marketing record older than a year should be deleted; a record
that must legally be kept, such as an invoice, stays longer.

## The data subject's rights

Laws give people rights over their own data: to **learn** whether their
data is processed and which data is held, to have it **corrected** if
wrong, to **ask for erasure** where conditions apply, and to **object** to
processing. Answering a person's question "what data do you hold about
me?" requires knowing where the data sits:

```python
TABLES = {
    "customers": [{"email": "ada@example.org"}, {"email": "bob@example.org"}],
    "orders": [{"email": "ada@example.org"}, {"email": "ada@example.org"}],
    "newsletter": [{"email": "bob@example.org"}],
}
person = "ada@example.org"
for table, rows in sorted(TABLES.items()):
    found = sum(1 for row in rows if row["email"] == person)
    if found:
        print(table, found)
```

```text
customers 1
orders 2
```

Without a **data inventory** showing which tables, systems and backups the
data sits in, this question cannot be answered with confidence.

## When there is a breach

When personal data leaks, the controller notifies the competent authority,
and the people affected where needed, within the short period set by law.
How this is done is part of the communication plan from the Incident
Response section.

## Summary

- **Privacy** is about how data is used in authorised hands; KVKK and the
  GDPR rest on the same basic principles.
- **Personal data** is any information about an identifiable person; data
  such as health is special category.
- Principles: purpose limitation, **data minimisation**, accuracy,
  **storage limitation**, security.
- A **pseudonym** reduces risk but the data stays personal; a keyed hash is
  used, not a plain one.
- Deleting the name is not anonymising: **k-anonymity** measures the
  indirect identifiers.
- The data subject's rights need a **data inventory**.
