# Rule-Based Information Extraction

So far we have given a whole text a single decision: positive or not, which
category, which topic. **Information extraction** pulls specific pieces out
of a text and puts them in a table: order number, amount, email, date, error
code, city. If a support ticket says "Order ORD-27246 says delivered", a
system can find that number and open the order record by itself. In this
section we extract information with rules, that is regular expressions
(regex) and lists, measure our rules on a small hand-labelled set, and put
the extracted information into a table.

## Extracting fields with regular expressions

For information with a known format, a regular expression is the shortest
way. In 02 we built the tokeniser with regex; this time we use the same tool
to find fields.

```python
import re

from text_data import make_tickets

PATTERNS = {
    "order": r"\bORD-\d{5}\b",
    "amount": r"\$\d+\.\d{2}",
    "email": r"\b[\w.]+@[\w.]+\.\w+\b",
    "date": r"\b\d{4}-\d{2}-\d{2}\b",
    "error": r"\bE\d{3,4}\b",
}


def extract(text):
    return {field: re.findall(p, text) for field, p in PATTERNS.items()}


tickets = make_tickets(2000)
print(tickets[4]["text"][:60])
print(extract(tickets[4]["text"]))
found = [extract(t["text"]) for t in tickets]
for field in PATTERNS:
    print(field, sum(bool(f[field]) for f in found))
```

```text
The app crashes every time I open the order page. Order ORD-
{'order': ['ORD-27246'], 'amount': [], 'email': [], 'date': [], 'error': []}
order 780
amount 261
email 173
date 46
error 191
```

- `\b` is a word boundary: so that `ORD-12345` is not torn out of a longer
  number such as `ORD-123456`.
- `\d{5}` is exactly five digits, `\d{3,4}` three or four. Error codes have
  three digits like `E401` or four like `E1007`.
- 780 of the 2000 tickets have an order number. These numbers are what was
  **found**; we do not know how many we missed. For that we need
  hand-labelled examples.

## Measuring a rule

The real problem with rules is that they catch the formats their writer
thought of. Our amount rule knows the `$12.49` format; what if `$5` or
`$1,200.00` comes along? Let us build a small **gold standard**: for each
sentence we write the right answer by hand.

```python
from collections import Counter

GOLD = [
    ("I paid $12.49 for it.", ["$12.49"]),
    ("Refund $5 please.", ["$5"]),
    ("The total was $1,200.00 in March.", ["$1,200.00"]),
    ("I was charged $8.90 and $8.90 again.", ["$8.90", "$8.90"]),
    ("It costs 30 dollars.", ["30 dollars"]),
    ("Version 2.49 of the app crashes.", []),
    ("Order ORD-12345 never came.", []),
]


def score(pattern):
    tp = fp = fn = 0
    for text, gold in GOLD:
        got, want = Counter(re.findall(pattern, text)), Counter(gold)
        tp += sum((got & want).values())
        fp += sum((got - want).values())
        fn += sum((want - got).values())
    return round(tp / (tp + fp), 3), round(tp / (tp + fn), 3)


print(score(r"\$\d+\.\d{2}"))
print(score(r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"))
```

```text
(1.0, 0.5)
(1.0, 0.833)
```

- When the first rule finds something it is always right (precision 1.0),
  but it finds only half of the amounts (recall 0.5): `$5` and `$1,200.00`
  are missed.
- The second rule knows the thousands separator (`(?:,\d{3})*`) and the
  optional cents (`(?:\.\d{2})?`): recall 0.833. "30 dollars" is still
  missed; an amount without a dollar sign needs a separate rule.
- We count with `Counter`, not with a set: if the same amount appears twice,
  it must be found twice.
- Writing rules is a loop: add new hard examples to the gold standard, widen
  the rule, measure that precision does not fall. A few hundred labelled
  examples from real text are the most valuable thing next to a rule.

## Putting information into a table

Once extracted information is in a table, ordinary data analysis starts:

```python
import pandas as pd

table = pd.DataFrame(found)
table["category"] = [t["category"] for t in tickets]
has_order = table["order"].str.len() > 0
print(has_order.groupby(table["category"]).mean().round(3))
errors = Counter(e for codes in table.loc[table["category"] == "technical", "error"]
                 for e in codes)
print(errors.most_common(3))
```

```text
category
account      0.120
billing      0.475
refund       0.641
shipping     0.669
technical    0.131
Name: order, dtype: float64
[('E500', 52), ('E401', 44), ('E403', 31)]
```

- Two thirds of shipping and refund tickets have an order number, but only
  one in eight account and technical tickets. Without an order number, a
  system cannot link a ticket to an order automatically; the form should ask
  for the number.
- The most common error code in technical tickets is `E500`: a server-side
  error. This information was buried inside ticket texts; once extracted, it
  became a number.

## Meaning from context

Two amounts of the same format can mean different things: money paid, or
money refunded? Let us look at the few words to the **left** of the amount:

```python
def amount_roles(text):
    roles = []
    for match in re.finditer(r"\$\d+\.\d{2}", text):
        left = text[max(0, match.start() - 30):match.start()].lower()
        roles.append("refund" if "refund" in left else "other")
    return roles


print(amount_roles("The refund of $20.00 has not reached my card."))
print(amount_roles("You refunded $10.00 but I paid more than that."))
print(Counter(r for t in tickets for r in amount_roles(t["text"])))
```

```text
['refund']
['refund']
Counter({'other': 193, 'refund': 80})
```

- If the 30-character left window contains "refund" or "refunded", the
  amount is a refund amount. 80 of the 273 amounts were marked as refunds.
- This is a rule too, and it has limits: in "I did not ask for a refund, I
  paid $20.00 twice" the window sees "refund" and gets it wrong. Context
  rules get complicated easily; at that point a sequence labelling model (the
  second note, and HMM in the next module) is a better way.

## Finding entities with a list

Some information has no format, only a name: cities, products, people. We
look these up with a **gazetteer** (a list of names). Let us find the cities
in the ticket data, then add "Nice" (a city in France) to the same list and
try it on the reviews:

```python
from text_data import CITIES, make_reviews

city_pattern = r"\b(" + "|".join(CITIES) + r")\b"
cities = Counter(m for t in tickets for m in re.findall(city_pattern, t["text"]))
print(cities.most_common(3))
reviews = [r["text"] for r in make_reviews(2000)]
print(sum(bool(re.search(r"\bNice\b", r, re.I)) for r in reviews))
print(sum(bool(re.search(r"\bNice\b", r)) for r in reviews))
```

```text
[('Berlin', 20), ('Madrid', 20), ('Dublin', 18)]
70
0
```

- We turned the list into a single regular expression with `|`; `\b` stops
  "Oslo" from being found inside "Oslonian".
- In case-insensitive search "Nice" was "found" in 70 reviews: all of them
  adjectives such as "the strap is very nice". Case-sensitive search finds 0;
  but only because in this data "nice" never starts a sentence. "Nice fit."
  at the start of a sentence would still count as a city.
- The list method is weak against **ambiguity**: "Paris" is a city and a
  name, "Apple" a company and a fruit. Telling them apart needs context.

## Finding a date, resolving a date

The date rule at the start found the `2026-03-14` format. Customers, though,
often write "tomorrow at 7pm". **Recognising** that phrase is easy, but
**resolving** it to a calendar time needs two more facts: the moment the
ticket was written (the reference time) and the time zone. The text itself
does not say either. Some phrases cannot be resolved even with them:
"tomorrow at 7" could be 7 in the morning or 7 in the evening. There the
right answer is not a date but a question to the user.

So the resolver returns one of three results: a date (accepted), `rejected`
(not recognised) or `needs_clarification`. We give the time zone as a fixed
offset, so the result is the same on every computer:

```python
from datetime import datetime, timedelta, timezone

ISTANBUL = timezone(timedelta(hours=3))
NOW = datetime(2026, 3, 14, 1, 30, tzinfo=ISTANBUL)  # ticket written at
TIME = r"(?P<day>today|tomorrow) at (?P<hour>\d{1,2})(?P<ampm>am|pm)?"


def resolve(phrase, now):
    m = re.fullmatch(TIME, phrase.lower().strip())
    if m is None:
        return "rejected"
    if m["ampm"] is None:
        return "needs_clarification"
    hour = int(m["hour"])
    if not 1 <= hour <= 12:
        return "rejected"
    hour = hour % 12 + (12 if m["ampm"] == "pm" else 0)
    day = now.date() + timedelta(days=1 if m["day"] == "tomorrow" else 0)
    when = datetime(day.year, day.month, day.day, hour, tzinfo=now.tzinfo)
    return when.isoformat()


PHRASES = ["tomorrow at 7pm", "tomorrow at 7", "today at 13pm", "next week"]
for phrase in PHRASES:
    print(f"{phrase:16} {resolve(phrase, NOW)}")
print(resolve("tomorrow at 7pm", NOW.astimezone(timezone.utc)))
```

```text
tomorrow at 7pm  2026-03-15T19:00:00+03:00
tomorrow at 7    needs_clarification
today at 13pm    rejected
next week        rejected
2026-03-14T19:00:00+00:00
```

- `re.fullmatch` needs the **whole** phrase to match; "next week" is a format
  the rule does not know, so instead of guessing it returns `rejected`.
- "tomorrow at 7" fits the rule, but morning or evening is unclear:
  `needs_clarification`. A perfectly formed answer can still be ambiguous in
  meaning.
- The last line gives the same moment in Greenwich time (UTC). At 01:30 at
  night in Istanbul it is still the evening of 13 March in UTC, so
  "tomorrow" becomes 14 March, not 15 March. The time zone changes the hour
  and even the day.
- `12am` is midnight and `12pm` is noon: `hour % 12` first turns 12 into 0.

Language is not enough for dates written in digits either. `03/04/2026` is
4 March in the US and 3 April in Turkey and most of Europe. A **policy**
decides which one it is, not the text:

```python
def read_numeric(text, policy):
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", text)
    if m is None:
        return "rejected"
    a, b, year = int(m[1]), int(m[2]), int(m[3])
    if policy == "US":
        month, day = a, b
    elif policy == "day-first":
        day, month = a, b
    elif a <= 12 and b <= 12 and a != b:
        return "needs_clarification"
    else:
        day, month = (a, b) if a > 12 else (b, a)
    try:
        return datetime(year, month, day).date().isoformat()
    except ValueError:
        return "rejected"


DATES = ["03/04/2026", "13/04/2026"]
for policy in ["US", "day-first", None]:
    print(policy, [read_numeric(d, policy) for d in DATES])
```

```text
US ['2026-03-04', 'rejected']
day-first ['2026-04-03', '2026-04-13']
None ['needs_clarification', '2026-04-13']
```

- With a policy, `03/04/2026` resolves to two different days. Without one,
  both numbers are 12 or less, so no choice can be made:
  `needs_clarification`.
- Under the US policy `13/04/2026` means month 13, which does not exist:
  `datetime` raises `ValueError` and the result is `rejected`. Without a
  policy, 13 cannot be a month, so it must be the day; the date is clear.
- The policy comes from outside the text: the user's setting, the company's
  country, the language of the form. If it is unknown, asking is better
  than booking the wrong day.

## Summary

- Information with a known format (numbers, amounts, emails, dates, codes) is
  extracted with regular expressions; `\b` and repeat counts (`{5}`, `{3,4}`)
  make a rule tighter.
- Measure a rule with precision and recall on a small hand-labelled gold
  standard; a rule only catches the formats you thought of.
- Once extracted information is in a table, ordinary analysis turns it into
  answers.
- Finding a date is not resolving it: the reference time, the time zone and
  the date order policy come from outside the text. The resolver returns a
  date, `rejected` or `needs_clarification`; when unsure, it asks.
- Context rules and lists give a quick start, but as ambiguity and context
  grow more complex, models that learn become necessary.
