# Improving Prompts Systematically

The most common way of improving a prompt is trial and error: add a
sentence, try a few messages, keep it if it looks good. This way falls into
two traps. First, "looking good" is not a measure; a change that fixes one
message may break two others. Second, a prompt that is fixed again and
again by looking at the same messages memorises those messages; it does not
show the same success on new messages.

In this section we turn the measurement we built in the Evaluating Prompts
section into a **loop**: measure, study the errors, make one change,
measure again. And we measure the most important rule of the loop: make
decisions with the **development set**, look at the **test set** once, at
the end.

## A toy model

To show the loop we have to be able to really run every prompt change; but
recorded replies exist only for the prompt they were written for. So in
this section we use a **toy model**. It is not a real language model: it
picks the category whose words, listed on the category's line in the
prompt, appear most often in the message, and says `unknown` if none
appears. The numbers are this toy's numbers; but the method (splitting the
set, studying errors, one change at a time, catching memorisation) is the
same with a real model.

We split the 40 messages in `shop_data` in two: the first 20 are the
development set (4 from each category), the last 20 the test set. We do not
touch the test set until the end of this section:

```python
import re

from shop_data import TICKETS


def render(definitions):
    lines = [f"- {label}: {', '.join(words)}"
             for label, words in definitions.items()]
    return "Classify the message into one category.\n" + "\n".join(lines)


def toy_model(prompt, text):
    words = set(re.findall(r"[a-z]+", text.lower()))
    best, best_hits = "unknown", 0
    for label, listed in re.findall(r"^- (\w+): (.+)$", prompt, re.M):
        hits = sum(word in words for word in listed.split(", "))
        if hits > best_hits:
            best, best_hits = label, hits
    return best


def accuracy(prompt, tickets):
    right = sum(toy_model(prompt, t["text"]) == t["label"] for t in tickets)
    return right / len(tickets)


DEV, TEST = TICKETS[:20], TICKETS[20:]
V1 = {"shipping": ["parcel", "delivery", "courier"],
      "returns": ["return", "exchange"],
      "refunds": ["refund", "refunded"],
      "warranty": ["warranty", "broke"],
      "payment": ["pay", "card", "checkout"]}
print(render(V1))
print("v1 dev accuracy", accuracy(render(V1), DEV))
for t in DEV:
    got = toy_model(render(V1), t["text"])
    if got != t["label"]:
        print(f"{t['id']:>2} {t['label']:<8} -> {got:<8} {t['text'][:36]}")
```

```text
Classify the message into one category.
- shipping: parcel, delivery, courier
- returns: return, exchange
- refunds: refund, refunded
- warranty: warranty, broke
- payment: pay, card, checkout
v1 dev accuracy 0.6
 2 returns  -> unknown  How do I send back a jacket that is 
 3 refunds  -> unknown  I returned my order two weeks ago an
 6 shipping -> unknown  The tracking page has not changed fo
 9 warranty -> unknown  A seam of my backpack is coming apar
11 shipping -> unknown  Do you deliver to Switzerland?
14 warranty -> unknown  The sole of my boots came off after 
15 payment  -> unknown  Do you accept bank transfer?
20 payment  -> unknown  I was charged twice for one order.
```

The prompt is built from the category definitions (`render`); so every
version is a dictionary and the difference between two versions is seen
exactly. The first version's accuracy on the development set is 0.6. This
is the **baseline**: every later change will be judged against it.

## Studying the errors

Making a change without reading the errors one by one is guessing. Here all
eight errors are of the same kind: the model says `unknown`, so none of the
words in the definitions is in the message. There is not a single "wrong
category" error. This tells us what to do: the definitions are too narrow.
Customers do not write "delivery", they write "deliver" or "tracking"; they
do not write "refund", they write "money".

Counting errors **by kind** (unknown, wrong category, format error) shows
which change will solve the most errors. The most crowded kind is dealt
with first.

## Generalising and memorising

Let us write two new versions. `v2` adds words that come from the
**meaning** of the categories: other forms of a word and common words that
describe the same situation. `v3` adds on top of `v2` words **copied
directly** from the remaining errors in the development set: "monday",
"switzerland", "boots", "twice"... These words have nothing to do with the
category; they only appear in those messages:

```python
from llm_client import count_tokens

V2 = {"shipping": V1["shipping"] + ["deliver", "delivered", "tracking", "arrived"],
      "returns": V1["returns"] + ["returning", "send", "back"],
      "refunds": V1["refunds"] + ["money"],
      "warranty": V1["warranty"] + ["broken", "stopped", "seam"],
      "payment": V1["payment"] + ["charged", "charge", "transfer"]}
V3 = {"shipping": V2["shipping"] + ["monday", "switzerland", "express"],
      "returns": V2["returns"] + ["small", "boots", "outlet"],
      "refunds": V2["refunds"] + ["returned", "weeks"],
      "warranty": V2["warranty"] + ["sole", "months", "zip"],
      "payment": V2["payment"] + ["twice", "instalments"]}
for name, version in [("v1", V1), ("v2", V2), ("v3", V3)]:
    prompt = render(version)
    dev, test = accuracy(prompt, DEV), accuracy(prompt, TEST)
    print(f"{name}: dev {dev:.2f}  test {test:.2f}  tokens {count_tokens(prompt)}")
```

```text
v1: dev 0.60  test 0.60  tokens 59
v2: dev 0.90  test 0.75  tokens 100
v3: dev 1.00  test 0.75  tokens 139
```

`v2` rose from 0.60 to 0.90 on the development set and to 0.75 on the test
set: words from the meaning helped on new messages too. `v3` reached 1.00
on the development set but stayed the same as `v2` on the test set (0.75):
the words it added fixed only those 20 messages. The gap between
development and test grew from 0.15 to 0.25; that is the sign of
memorisation (overfitting). Moreover, `v3` is 139 tokens on every call and
`v2` 100: 39 tokens that bring no success are paid on every call. `v2`
itself has a gap too (0.90 against 0.75), because it was also written by
looking at the errors of the development set. The success measured on the
development set is always a little optimistic; the final measure is taken
from a set that has never been looked at. Here we looked at the test set
for three versions because the goal is to show the difference; in real
work only the chosen version is looked at.

## Which part helps?

As a prompt grows, it becomes unclear which of its parts really helps. The
way to measure this is **ablation**: taking each part out one at a time
and measuring again. If the success falls when a part is taken out, the
part helps; if it does not, at least it adds nothing on this set. Let us
take out the words added in `v2` one at a time:

```python
def without(definitions, label, word):
    return {key: [w for w in words if (key, w) != (label, word)]
            for key, words in definitions.items()}


base = accuracy(render(V2), DEV)
useless = []
for label, words in V2.items():
    for word in words:
        if word in V1[label]:
            continue
        change = accuracy(render(without(V2, label, word)), DEV) - base
        if change:
            print(f"without {word:<9} {label:<9} {change:+.2f}")
        else:
            useless.append(word)
print("no effect on dev:", ", ".join(useless))
pair = without(without(V2, "returns", "send"), "returns", "back")
print("without send and back:")
for t in DEV:
    old, new = toy_model(render(V2), t["text"]), toy_model(render(pair), t["text"])
    if old != new:
        print(f"  {t['id']:>2} {t['label']:<8} {old} -> {new}")
```

```text
without deliver   shipping  -0.05
without tracking  shipping  -0.05
without back      returns   +0.05
without seam      warranty  -0.05
without charged   payment   -0.05
without transfer  payment   -0.05
no effect on dev: delivered, arrived, returning, send, money, broken, stopped, charge
without send and back:
   2 returns  returns -> unknown
   3 refunds  returns -> refunds
```

Taking out five words lowers the success by 0.05: each of them saves one
message on its own. Taking out `back`, however, **raises** the success:
message 3 ("...no money back") was counted as a return instead of a refund
because of `back`. Eight words have no effect on their own on this set. But
"no effect" can mean two things: the word does not appear in these 20
messages at all, or another word next to it does the same job. Taking out
`send` and `back` together leaves the total unchanged but changes the
answers of two messages: one breaks (2), one is fixed (3). The answers can
change while the total stays the same; that is why changes are compared
message by message. Before deleting a part that came out "useless" on a
small set, it needs to be measured on a larger set.

## The loop

Let us turn the whole section into a way of working:

1. **Build the evaluation set** and split it in two: development and test.
   Both sets should have enough examples of every category.
2. **Measure the baseline** and record it.
3. **Read the errors** and count them by kind. Start with the most crowded
   kind.
4. **Make one change.** If two changes are made together, it is not known
   which one helped (or which one broke something).
5. **Measure again on the development set.** Look not only at the total
   success but also at whether any answer that was right before broke (the
   comparison in the Evaluating Prompts section).
6. **Write it in the log:** version, change, reason, measure. The version
   digest from the System Messages section is useful here.
7. When it is good enough, **look at the test set once.** If you fix the
   prompt again according to the test result, the test set becomes a
   development set; from then on, a reliable measure needs new messages
   that have never been looked at.

Small sets also carry uncertainty: in 20 messages one message is 5 points.
A difference of 0.05 means a single message; that is why the bootstrap
interval from the Evaluating Prompts section matters.

## Summary

- A loop instead of trial and error: measure, read the errors, one change,
  measure again, write the log.
- Decisions are made with the development set; the test set is looked at
  once, at the end.
- Details copied from the messages in the development set raise the success
  on that set but not on new messages: memorisation. The gap between
  development and test shows it.
- Errors are counted by kind; the most crowded kind comes first.
- Ablation shows which part helps; parts that look useless when taken out
  one at a time may matter together, and "useless" on a small set is weak
  evidence.
- A longer prompt means more tokens on every call; an addition that brings
  no success is a cost.
