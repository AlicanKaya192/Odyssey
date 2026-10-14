# Evaluating Prompts

In this module we have seen many prompt principles: clear instructions,
examples, structured output, the system message. With each we gave the
same warning: you can only learn whether a principle helps **on your
model** by measuring. This section is about how that measuring is done:
building an **evaluation set**, scoring the answers of two prompt versions
on the same set, splitting the errors into kinds, and checking whether
the difference between two versions is real or chance.

## The evaluation set and recorded answers

An evaluation set is inputs whose right answer is known: here the 40
support messages in `shop_data.py` and the categories an employee gave
them. In a real project you ask the model every message with every prompt
version, record the answers and score the records.

Because this lesson cannot connect to a real model, `shop_data.py` holds
the answers of two prompt versions (`v1`: instruction only, `v2`: with
examples and a clear format) to the 40 messages as **example replies
written for the lesson**. The numbers below are the scores of these
example replies; they are not a measurement of a model. What you learn is
the scoring method; on your own model you apply the same code to your own
records.

## Three separate measures

When scoring an answer, three questions are asked separately: is the
answer exactly in the wanted form, can the program parse it, and is the
parsed value right?

```python
from collections import Counter

from shop_data import TICKETS, LABELS, RECORDED


def normalize(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


gold = [t["label"] for t in TICKETS]
for version, replies in RECORDED.items():
    exact = sum(r == g for r, g in zip(replies, gold))
    parsed = [normalize(r) for r in replies]
    valid = sum(p != "needs_review" for p in parsed)
    right = sum(p == g for p, g in zip(parsed, gold))
    print(f"{version}: exact {exact}/40  valid {valid}/40  right {right}/40")
```

```text
v1: exact 26/40  valid 36/40  right 31/40
v2: exact 35/40  valid 39/40  right 36/40
```

Only 26 of `v1`'s 40 answers are exactly in the wanted form. After the
strict parser cleans harmless differences, 36 can be parsed and 31 are
right. `v2` has 35 exact, 39 parsable and 36 right. Counting form and
correctness separately matters: part of `v1`'s shortfall is not wrong
categories but sentences such as "It is about payment." that cannot be
parsed. A format problem is fixed by the format instruction and examples;
a wrong category by the definitions of the categories.

## The kinds of errors

The total score does not say what to fix. Let us count which category was
mixed up with which:

```python
for version, replies in RECORDED.items():
    parsed = [normalize(r) for r in replies]
    misses = Counter((g, p) for g, p in zip(gold, parsed) if g != p)
    print(version)
    for (truth, answer), count in misses.most_common():
        print(f"   {truth:8} -> {answer:12} {count}")
```

```text
v1
   refunds  -> payment      2
   payment  -> needs_review 1
   returns  -> needs_review 1
   refunds  -> shipping     1
   payment  -> refunds      1
   shipping -> needs_review 1
   shipping -> payment      1
   refunds  -> needs_review 1
v2
   refunds  -> payment      1
   refunds  -> needs_review 1
   payment  -> refunds      1
   warranty -> returns      1
```

In both versions the most confused pair is refunds and payment
(`refunds` ↔ `payment`): messages such as "I was charged twice" or "I paid
with a gift card" look like both categories. This says what to add to the
prompt: a sentence explaining the difference between the two categories
and an example of such a message. `v1`'s four `needs_review` come from a
single problem: the answer's form.

## Is the difference real?

Forty messages is a small set. The difference between two versions may
depend on the luck of a few messages. We look at two things: the messages
where the versions give **different** results (the ones answered the same
way do not explain the difference), and the range of the difference with
the **resampling** (bootstrap) we saw in the previous module.

```python
import random

ok1 = [normalize(r) == g for r, g in zip(RECORDED["v1"], gold)]
ok2 = [normalize(r) == g for r, g in zip(RECORDED["v2"], gold)]
print("only v2 right:", sum(b and not a for a, b in zip(ok1, ok2)))
print("only v1 right:", sum(a and not b for a, b in zip(ok1, ok2)))
rng = random.Random(0)
diffs = []
for _ in range(2000):
    picks = [rng.randrange(40) for _ in range(40)]
    diffs.append(sum(ok2[i] - ok1[i] for i in picks) / 40)
diffs.sort()
print("difference", (sum(ok2) - sum(ok1)) / 40,
      "90% interval", diffs[100], diffs[1899])
```

```text
only v2 right: 7
only v1 right: 2
difference 0.125 90% interval 0.0 0.25
```

The versions give different results on 9 of the 40 messages: on 7 only
`v2` is right, on 2 only `v1`. The difference is 0.125 (five messages),
but the resampling 90% interval is between 0 and 0.25 and its lower end
is zero. `v2` looks ahead, but this set does not settle the difference;
it needs measuring with more messages. On a forty-message set even a
five-message difference moves this much.

## When a model scores another model

In jobs with one right answer, such as a category, scoring is done with
code. For open-ended jobs, such as whether a summary is good, a common way
is to give another model call a **rubric** and have it score the answer
("model as a judge"). This way is fast, but the scorer is a model too:

- The scorer may have its own biases: it may favour long answers or
  answers in a style like its own.
- Do not trust the scorer's decisions before comparing them with **human
  labels**; measure the agreement between the scorer and people, as we
  measured the agreement of two annotators in the previous module.
- Write the rubric clearly: not "is it good?" but separate questions such
  as "is the product named, is there a promise, does it answer the
  question?".

## When building an evaluation set

- **Build it from real inputs** and add the hard cases: messages between
  two categories, questions with no answer, malicious messages.
- **Do not change the set, grow it.** To compare with old versions, new
  examples are added to the same set and old ones are not deleted.
- **Keep a development set and a test set apart.** If you improve the
  prompt on one set, the score on that set becomes optimistic; make the
  final decision with a test set you never looked at (in the Systematic
  Improvement section).
- **Run it again with every prompt change.** A fix in one place can break
  another (a regression).

## Summary

- An evaluation set is inputs with known right answers; every prompt
  version is scored on the same set.
- Form, parsability and correctness are measured separately.
- Split the errors into kinds; the kinds of errors, not the total score,
  say what to fix.
- On a small set a difference can be chance: look at the messages where
  the versions differ and at the range with resampling.
- A model scoring another model is fast but is first compared with human
  labels.
- Grow the set, keep development and test sets apart, run again with
  every change.
