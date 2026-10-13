Accuracy is a single number: it says how many predictions were right but not
**which** mistakes were made. The simplest way to understand the mistakes is
to count every (true label, prediction) pair.

```python
from collections import Counter

pairs = Counter((r["label"], predict(r["text"])) for r in reviews)
for label in ["positive", "neutral", "negative"]:
    row = [pairs[(label, guess)] for guess in ["positive", "neutral", "negative"]]
    print(label.ljust(8), row, sum(row))
```

```text
positive [528, 687, 103] 1318
neutral  [28, 239, 22] 289
negative [79, 183, 131] 393
```

This is the error table of the `predict` rule from the lesson. Each row is a
**true** label; the columns are the rule's `positive`, `neutral` and
`negative` predictions in that order. The diagonal (top left to bottom
right: 528, 239, 131) holds the correct predictions; they add up to 898, the
number from the lesson.

## What does the table say?

- **687 positive reviews were called "neutral".** This is the biggest
  problem: most positive reviews contain none of the words on our lists
  ("It does the job", "Much better"), so the score stays at 0.
- **103 positive reviews were called "negative".** Most of them are
  negation: "not bad", "not fragile".
- **183 negative reviews were called "neutral".** Sentences such as "would
  not buy" and "Returned it" are on no list.
- The rule looks good on neutral reviews (239 of 289), but this is not a
  success: the rule calls everything it is unsure about "neutral" anyway.

The last point matters: a high hit rate in one class can also come from the
model piling everything into that class. The ideas that measure this
(**precision** and **recall**) come in section 09, where this table also gets
its proper name: the **confusion matrix**.

## A habit

After every model you try, do not look at accuracy alone:

1. Build the error table.
2. Read a few examples from the biggest error cell.
3. Name the cause of the mistake (negation, a missing word, a typo).

These causes decide which method you try next.
