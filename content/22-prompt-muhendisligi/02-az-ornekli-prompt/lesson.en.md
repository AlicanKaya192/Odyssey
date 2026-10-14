# Zero-Shot and Few-Shot Prompting

There are two ways to explain a job: state the rule or show examples. A
prompt that only gives an instruction is called **zero-shot**; one that
adds a few solved examples is called **few-shot**. The examples show the
model both the task and the form of the answer: instead of saying "the
category name only", you show a few answers that are just a category
name. In this section we build a few-shot prompt in code and focus on
the real question: **which examples** should go in? That question depends
on the data, not on the model, and it can really be measured here.

## Data: labelled support messages

`shop_data.py` holds 40 support messages of an outdoor shop and the
category an employee gave them; the messages were written by hand for the
lessons. First we split them into two parts: the **pool** we pick
examples from and the **test** messages we try the prompt on. The two
must never mix; if a test message also sits in the prompt as an example,
the prompt looks better than it is.

```python
from collections import Counter

from shop_data import TICKETS, LABELS

test = [t for t in TICKETS if t["id"] % 4 == 0]
pool = [t for t in TICKETS if t["id"] % 4 != 0]
print(len(pool), "examples to choose from,", len(test), "for testing")
print(Counter(t["label"] for t in test))
print(pool[0]["text"], "->", pool[0]["label"])
```

```text
30 examples to choose from, 10 for testing
Counter({'warranty': 2, 'refunds': 2, 'returns': 2, 'shipping': 2, 'payment': 2})
My parcel should have arrived on Monday. Where is it? -> shipping
```

## Examples as messages

One way to put examples into the prompt is to give them as if they were
the conversation's history: each example is a `user` message and its
`assistant` answer. The model sees the exact form of the answer (a
single lower-case word) from these answers.

```python
from llm_client import ChatClient, count_message_tokens

SYSTEM = ("Put the customer message into one category: "
          + ", ".join(LABELS) + ". Answer with the category only.")


def build_messages(examples, text):
    messages = [{"role": "system", "content": SYSTEM}]
    for example in examples:
        messages.append({"role": "user", "content": example["text"]})
        messages.append({"role": "assistant", "content": example["label"]})
    messages.append({"role": "user", "content": text})
    return messages


question = test[0]["text"]
for k in [0, 2, 5, 10]:
    tokens = count_message_tokens(build_messages(pool[:k], question))
    print(k, "examples:", tokens, "tokens")

client = ChatClient(["warranty"])
client.chat(build_messages(pool[:2], question), max_tokens=5)
print([m["role"] for m in client.calls[0]["messages"]])
```

```text
0 examples: 56 tokens
2 examples: 107 tokens
5 examples: 178 tokens
10 examples: 287 tokens
['system', 'user', 'assistant', 'user', 'assistant', 'user']
```

Every example, with its message and answer, is sent again in every call;
the token count grows linearly with the number of examples. Ten examples
are 5.1 times the zero-shot prompt. Examples are not free, so
we want few but well-chosen ones.

Examples can also be written inside a single text (`Message: ...
Category: ...` lines). Which works better on your model is a question of
measurement; the message form is the common one for chat models.

## Random examples miss categories

The easiest way is to draw five random examples from the pool. With five
categories and five examples, is that enough to show every category? Let
us count over a thousand different draws:

```python
import random

missing = 0
for seed in range(1000):
    picked = random.Random(seed).sample(pool, 5)
    missing += len({t["label"] for t in picked}) < len(LABELS)
print("random draws missing a category:", missing, "of 1000")


def balanced(pool, per_label, seed):
    rng = random.Random(seed)
    chosen = []
    for label in LABELS:
        same = [t for t in pool if t["label"] == label]
        chosen += rng.sample(same, per_label)
    rng.shuffle(chosen)
    return chosen


print([t["label"] for t in balanced(pool, 1, seed=3)])
```

```text
random draws missing a category: 932 of 1000
['returns', 'shipping', 'refunds', 'warranty', 'payment']
```

Five random examples leave at least one category out in almost every
draw. The balanced choice takes the same number of examples from each
category and then shuffles them. Shuffling matters: if the examples
stayed sorted by category, the last example would always have the same
category. It is known that the order and the label distribution of the
examples can affect the answer; how much depends on the model, so giving
them balanced and shuffled is a safe default.

## Examples that look like the input

Another way is to pick, for each new message, the examples from the pool
that **look most like it**. TF-IDF and cosine similarity, which we used to
search documents in the previous module, help here too:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer().fit([t["text"] for t in pool])
pool_vectors = vectorizer.transform([t["text"] for t in pool])


def similar(text, k):
    scores = (pool_vectors @ vectorizer.transform([text]).T).toarray().ravel()
    best = scores.argsort()[::-1][:k]
    return [pool[i] for i in best]


for t in test[:2]:
    print(t["label"], "|", t["text"])
    for e in similar(t["text"], 3):
        print("    ", e["label"], "|", e["text"])
same = sum(similar(t["text"], 1)[0]["label"] == t["label"] for t in test)
print("nearest example has the same category:", same, "of", len(test))
```

```text
warranty | The zip of my tent broke after one year.
     warranty | The sole of my boots came off after three months.
     warranty | A seam of my backpack is coming apart.
     shipping | Can I change the delivery address after ordering?
refunds | When will the refund reach my credit card?
     refunds | I paid with a gift card, how do I get my refund?
     payment | My card was declined at checkout.
     refunds | Can the refund go to a different bank account?
nearest example has the same category: 6 of 10
```

For the first message two of the three most similar examples are from
the same category (`warranty`), but the shared words are mostly common
ones such as "the", "of", "my", "after"; the third example is a shipping
message. Over all test messages the nearest example has the same
category for 6 of ten. Word overlap is a weak measure of similarity: it
cannot find two messages that mean nearly the same thing with different
words. For similarity of meaning, embedding models are used; they too
are chosen by measuring in the same way.

Picking similar examples has two prices. First, every message needs its
own search. Second, the chosen examples may all come from one category,
and the prompt then shows only that category. In practice the two ways
are combined: for example, the most similar example from each category.

## A checklist for choosing examples

- **Do not use test messages as examples.** Keep the pool and the test
  apart; otherwise the success you measure is memorisation.
- **Show every category** and give the examples in a shuffled order.
- **Write the example answers exactly in the wanted form.** If one
  example answer is written "Shipping.", the model learns that form too.
- **Pick few but good ones.** Every example is paid in every call;
  measure whether adding examples is worth it.
- **Show the hard cases with examples.** Messages between two categories
  (a refund or a return?) are the most useful examples.

## Summary

- A zero-shot prompt only gives an instruction; a few-shot prompt also
  shows solved examples and teaches the answer's form by example.
- Examples can be given as `user` / `assistant` message pairs; each is
  paid again in every call.
- Five random examples missed at least one of five categories in almost
  every draw; a balanced and shuffled choice prevents this.
- Examples that look like the input can be found with TF-IDF; they can
  upset the category balance, and the two ways can be combined.
- The example pool and the test messages are kept apart.
