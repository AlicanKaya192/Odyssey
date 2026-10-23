# Structured Output and Validation

So far we asked the model for a single word or a single number. Most
applications want more than one piece of information: a support
message's category, whether it is urgent, the order number in it. Asking
for these as free text forces the program to search the text in every
answer. Instead we ask for the answer in a **structured** form, usually
JSON. In this section we parse the incoming JSON step by step, validate
it against a schema and, when the answer is invalid, tell the model the
error and ask again.

## Writing the schema

In the instruction we state the exact form of the answer, field by
field:

<figure class="fig anat">
  <div class="anat-row"><span><code>category</code></span><span>One of these five: shipping, returns, refunds, warranty, payment</span></div>
  <div class="anat-row"><span><code>urgent</code></span><span><code>true</code> or <code>false</code></span></div>
  <div class="anat-row"><span><code>order_id</code></span><span><code>ORD-</code> and five digits, <code>null</code> if the message has none</span></div>
</figure>

The instruction also ends with "Write only the JSON object, add no other
text". Some chat APIs offer a setting that forces the answer to be valid
JSON or to follow a given schema; use it if your service has one. But
that setting only guarantees the **form**; your program still checks
whether the category was chosen correctly.

## The answer is not always clean JSON

The six **example replies** below stand for answers such an instruction
could get: clean JSON, JSON wrapped in a code block, JSON with a sentence
in front, an object written with single quotes like a Python dictionary,
JSON with the right form but wrong values, and JSON cut off at
`max_tokens`. Our parser tries three ways in order: the text itself, the
text with the code block marks removed, and the part between the first
`{` and the last `}`.

```python
import json
import re

FENCE = "`" * 3
REPLIES = [
    '{"category": "shipping", "urgent": true, "order_id": "ORD-48213"}',
    FENCE + 'json\n{"category": "refunds", "urgent": false, '
    '"order_id": null}\n' + FENCE,
    'Sure! Here is the JSON:\n{"category": "warranty", '
    '"urgent": false, "order_id": "ORD-10077"}',
    "{'category': 'payment', 'urgent': True, 'order_id': None}",
    '{"category": "delivery", "urgent": "yes", "order_id": "48213"}',
    '{"category": "returns", "urgent": false, "order_id": "ORD-',
]


def parse_json(text):
    attempts = {
        "as is": text,
        "fence": re.sub(r"^`{3}(?:json)?\s*|\s*`{3}$", "", text.strip()),
        "braces": text[text.find("{"): text.rfind("}") + 1],
    }
    for name, candidate in attempts.items():
        try:
            return json.loads(candidate), name
        except json.JSONDecodeError:
            pass
    return None, "failed"


for number, reply in enumerate(REPLIES, 1):
    print(number, parse_json(reply)[1])
```

```text
1 as is
2 fence
3 braces
4 failed
5 as is
6 failed
```

Four of the six answers were parsed one way or another. The code block
and the sentence in front are harmless additions; removing them is safe.
The single-quoted object is not JSON; rescuing it with Python's own
reader is possible, but then it becomes unclear which forms are
accepted, and asking again is cleaner. The cut-off answer cannot be
rescued at all: here you must look at `finish_reason` first; if it is
`length`, `max_tokens` was not enough for the answer.

## Validating against the schema

Not every parsed JSON is right. The fifth answer is valid JSON, but the
category is not in the list, `urgent` is text and the order number has
the wrong form. Let us turn the schema into code:

```python
LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def validate(data):
    if not isinstance(data, dict):
        return ["the answer must be a JSON object"]
    errors = [f"missing {key}" for key in ["category", "urgent", "order_id"]
              if key not in data]
    if data.get("category") not in LABELS:
        errors.append("category must be one of " + ", ".join(LABELS))
    if not isinstance(data.get("urgent"), bool):
        errors.append("urgent must be true or false")
    order = data.get("order_id")
    if order is not None and not re.fullmatch(r"ORD-\d{5}", str(order)):
        errors.append("order_id must look like ORD-12345 or be null")
    return errors


for number, reply in enumerate(REPLIES, 1):
    data, stage = parse_json(reply)
    errors = validate(data) if data is not None else ["not valid JSON"]
    print(number, "ok" if not errors else f"{len(errors)} error(s)")
print(*validate(parse_json(REPLIES[4])[0]), sep="\n")
```

```text
1 ok
2 ok
3 ok
4 1 error(s)
5 3 error(s)
6 1 error(s)
category must be one of shipping, returns, refunds, warranty, payment
urgent must be true or false
order_id must look like ORD-12345 or be null
```

Only three of the six answers can be used. We wrote the error messages
deliberately as **readable sentences**: in the next step we will send
them to the model.

## Telling the error and asking again

When an invalid answer comes, the simplest repair is to add the model's
answer and the error list to the conversation and ask again. The model
sees what it did wrong. Instead of trying without end, we set an upper
limit:

```python
import textwrap

from llm_client import ChatClient, count_message_tokens


def ask_json(client, messages, max_tries=3):
    messages = list(messages)
    for tries in range(1, max_tries + 1):
        reply = client.chat(messages, max_tokens=60)
        data, stage = parse_json(reply.text)
        errors = validate(data) if data is not None else ["not valid JSON"]
        if not errors:
            return data, tries
        feedback = ("Your answer was not valid: " + "; ".join(errors)
                    + ". Reply with the JSON object only.")
        messages += [{"role": "assistant", "content": reply.text},
                     {"role": "user", "content": feedback}]
    return None, max_tries


client = ChatClient([REPLIES[4], REPLIES[0]])
question = [{"role": "user", "content": "My parcel ORD-48213 is late!"}]
data, tries = ask_json(client, question)
print(data, tries)
print(textwrap.fill(client.calls[1]["messages"][-1]["content"], 64))
print([count_message_tokens(call["messages"]) for call in client.calls])
```

```text
{'category': 'shipping', 'urgent': True, 'order_id': 'ORD-48213'} 2
Your answer was not valid: category must be one of shipping,
returns, refunds, warranty, payment; urgent must be true or
false; order_id must look like ORD-12345 or be null. Reply with
the JSON object only.
[16, 114]
```

A valid answer came on the second try. The repair has a price too: the
second call sends the first question, the wrong answer and the error
message together; the input went from 16 to 114 tokens. That is why you
first improve the instruction and the examples to reduce invalid answers
and use the repair only for the cases that remain. If the limit of tries
is reached, the answer goes to a person or a default path
(`needs_review`).

## An answer that passes the schema but is ambiguous

A schema checks the form, not the meaning. Say a customer writes "Call me
tomorrow at 7". While extracting a callback time, the model cannot know
whether that is morning or evening, but because the schema asks for a time
it still **picks** one: `"07:00"`. The answer is flawless JSON and passes
the schema, yet the right answer is to ask the customer. As we saw in the
Information Extraction section of NLP Fundamentals, "tomorrow" only
becomes a day once today is known; so we give the model the reference
time as **context** and also ask for the source of the answer, the
customer's own words (`source`).

The five **example replies** below are answers that such an instruction
could get. The program sorts each one into one of three results:
`accepted`, `rejected` or `needs_clarification`:

```python
import json
from collections import Counter
from datetime import datetime, timedelta

NOW = "2026-03-14T01:30:00+03:00"
SYSTEM = ("Extract the callback time as JSON with date (YYYY-MM-DD), "
          "time (HH:MM, 24-hour) and source (the customer's exact words). "
          "The current time is " + NOW + ".")
CASES = [  # customer message, example reply, expected result
    ("Call me tomorrow at 7pm.",
     '{"date": "2026-03-15", "time": "19:00", "source": "tomorrow at 7pm"}',
     "accepted"),
    ("Call me tomorrow at 7.",
     '{"date": "2026-03-15", "time": "07:00", "source": "tomorrow at 7"}',
     "needs_clarification"),
    ("Call me today at 9am.",
     '{"date": "2026-03-15", "time": "09:00", "source": "today at 9am"}',
     "rejected"),
    ("Please call me back.",
     '{"date": "2026-03-14", "time": "10:00", "source": "today at 10am"}',
     "rejected"),
    ("Tomorrow at 12pm works.",
     '{"date": "2026-03-15", "time": "12:00", "source": "Tomorrow at 12pm"}',
     "accepted"),
]
PHRASE = r"(today|tomorrow) at (\d{1,2})(am|pm)?"
KEYS = {"date", "time", "source"}


def schema_only(message, data, now):
    keys_ok = isinstance(data, dict) and set(data) == KEYS
    return "accepted" if keys_ok else "rejected"


def check_callback(message, data, now):
    if schema_only(message, data, now) == "rejected":
        return "rejected"
    m = re.fullmatch(PHRASE, str(data["source"]).lower())
    if m is None or str(data["source"]).lower() not in message.lower():
        return "rejected"
    if m[3] is None:
        return "needs_clarification"
    hour = int(m[2]) % 12 + (12 if m[3] == "pm" else 0)
    days = 1 if m[1] == "tomorrow" else 0
    day = datetime.fromisoformat(now).date() + timedelta(days=days)
    if (data["date"], data["time"]) != (day.isoformat(), f"{hour:02d}:00"):
        return "rejected"
    return "accepted"


client = ChatClient([reply for _, reply, _ in CASES])
outcomes = []
for message, _, expected in CASES:
    question = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": message}]
    data, stage = parse_json(client.chat(question, max_tokens=60).text)
    got = check_callback(message, data, NOW)
    outcomes.append((expected, schema_only(message, data, NOW), got))
    print(f"{message:25} {got}")
totals = Counter(e for e, _, _ in outcomes)
print(f"{'':20} schema  check")
for label in ["accepted", "rejected", "needs_clarification"]:
    schema = sum(e == s for e, s, _ in outcomes if e == label)
    check = sum(e == g for e, _, g in outcomes if e == label)
    print(f"{label:20} {schema}/{totals[label]}     {check}/{totals[label]}")
```

```text
Call me tomorrow at 7pm.  accepted
Call me tomorrow at 7.    needs_clarification
Call me today at 9am.     rejected
Please call me back.      rejected
Tomorrow at 12pm works.   accepted
                     schema  check
accepted             2/2     2/2
rejected             0/2     2/2
needs_clarification  0/1     1/1
```

- All five answers are valid JSON with the three fields of the schema. A
  check that looks only at the schema (the `schema` column) accepts all
  five: it misses the two answers that should be rejected and the one that
  should be asked about.
- In the second answer the model made up `"07:00"`. The customer's words
  have no `am`/`pm`; the program sees this in the source and chooses to
  ask.
- In the third the model turned "today" into 15 March; the program does
  the same calculation itself with the reference time and rejects the
  answer when they differ. In the fourth the `source` does not appear in
  the customer's message at all: the model made the time up.
- We count the results **separately**. A single accuracy rate does not
  tell an error that "accepts" a case needing clarification from one that
  accepts an answer that should be rejected; the two cost different
  things.

## Summary

- If more than one piece of information is wanted, ask for the answer in
  a structured form such as JSON and write the schema field by field.
- When parsing, clean harmless additions (a code block, a sentence in
  front); do not rescue what is not JSON with a guess.
- The cause of cut-off JSON is `max_tokens`; look at `finish_reason`
  first.
- Validate the parsed data against the schema: fields, types, allowed
  values, patterns.
- Write errors as readable sentences and ask again by sending them to the
  model when an answer is invalid; limit the number of tries.
- The repair sends more tokens with every try; the real fix is a clear
  instruction that reduces invalid answers.
- Passing the schema does not show the meaning is right. Give the model
  context such as the reference time, ask for the source and let the
  program check it; do not accept an ambiguous answer, ask. Measure the
  accepted, rejected and needs-clarification cases separately.
