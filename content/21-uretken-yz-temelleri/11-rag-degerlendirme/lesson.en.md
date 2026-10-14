# Evaluating RAG

In the previous section the RAG setup answered some questions correctly and got
others wrong. A single number like "accuracy 62%" does not say what to fix:
does the error come from the search or from the reading? This section shows how
to measure a RAG system **piece by piece**: first retrieval, then the answer,
then abstaining; and finally the limits of a small evaluation set.

## The evaluation set

We have 27 questions. For each, the article that answers it and the phrase
that must appear in a correct answer (`key`) are written down; three have no
answer in the documents. Such a set is built by choosing real user questions
and labelling them by hand, and every time the system changes it is measured
again on the same set. The setup from 10 is in the file `rag_tools.py`.

## 1. Measuring retrieval

We look at the position (**rank**) of the first chunk containing the answer
phrase. Two measures:

- **recall@k:** the share of questions whose phrase is in the first `k`
  chunks.
- **MRR** (mean reciprocal rank): `1 / rank` for every question (0 if it was
  never found), averaged over the questions. If the right chunk is first it is
  1, if second 0.5; a search that puts the right chunk on top is rewarded.

```python
from rag_tools import index, rag, NOT_FOUND, QUESTIONS

answerable = [q for q in QUESTIONS if q["doc"]]


def first_rank(question, key, k=10):
    found = index.search(question, k)
    for rank, ((_, text), _) in enumerate(found, 1):
        if key in text:
            return rank
    return None


ranks = [first_rank(q["q"], q["key"]) for q in answerable]
for k in [1, 3, 5, 10]:
    hits = sum(r is not None and r <= k for r in ranks)
    print(f"recall@{k:<2}", round(hits / len(ranks), 2))
print("MRR", round(sum(1 / r for r in ranks if r) / len(ranks), 2))
```

```text
recall@1  0.71
recall@3  0.71
recall@5  0.75
recall@10 0.96
MRR 0.75
```

The right sentence is first for 71% of the questions, and the share is the same
for the first three: what is not first does not appear second or third either.
Looking at the first 10 chunks the share rises to 96%; the right sentence is
usually in the list, but further down. MRR is 0.75.

## 2. Finding where the error is

Let us put every wrong or missed answer into one of two groups: if the right
chunk is **not** among the first three sources it is a retrieval error, if it
**is** there it is a reading error.

```python
table = {"correct": 0, "retrieval miss": 0, "reading error": 0}
for q, rank in zip(answerable, ranks):
    reply = rag(q["q"], 3, 2)
    if q["key"] in reply.text:
        table["correct"] += 1
    elif rank is None or rank > 3:
        table["retrieval miss"] += 1
    else:
        table["reading error"] += 1
print(table)
```

```text
{'correct': 15, 'retrieval miss': 7, 'reading error': 2}
```

Seven of the nine missed answers are retrieval errors: the right sentence is
not among the first three sources, and whatever the reader does it cannot find
the answer. Only two are reading errors. So in this system the first job is to
improve the search (09: embedding or hybrid search); working on the prompt or
the model could save at most two questions. A single accuracy number would not
have shown this.

## 3. Measuring abstention

The "not found" answer is a prediction too: recognising a question that has no
answer. We ask two questions: when it says "not found", how often is it right
(**precision**), and how many of the questions without an answer does it
recognise (**recall**)?

```python
for min_overlap in [1, 2, 3]:
    said = right = 0
    for q in QUESTIONS:
        if rag(q["q"], 3, min_overlap).text == NOT_FOUND:
            said += 1
            right += q["key"] is None
    unanswerable = sum(q["key"] is None for q in QUESTIONS)
    print(f"overlap>={min_overlap} said not found {said:2}",
          f"precision {right / said:.2f} recall {right / unanswerable:.2f}")
```

```text
overlap>=1 said not found  3 precision 0.33 recall 0.33
overlap>=2 said not found 10 precision 0.30 recall 1.00
overlap>=3 said not found 25 precision 0.12 recall 1.00
```

At threshold 2 all three questions with no answer are recognised (recall
1.00), but only 30% of the "not found" answers go to questions that really
have no answer; the other seven are questions that do. At threshold 3, 25 of
the 27 questions get "not found": recall is again 1.00, but the system answers
almost nothing and precision drops to 0.12. At threshold 1 "not found" is said
only three times and one of them is right. Someone looking only at recall
could take a system that says "not found" to everything for perfect; the two
measures are read together.

## 4. The limit of a small set

With 24 answerable questions, **one** question is worth 4.2 points. In 10,
threshold 1 gave two more correct answers than threshold 2 (17 against 15). Is
this difference reliable? Let us look by **resampling** the questions
(bootstrap): we draw the 24 questions 24 times with replacement and compute the
difference in correct answers between the two settings 2000 times. The
distribution of the difference gives an idea of what we might see on another
set of 24 questions.

```python
import numpy as np


def correct_vector(min_overlap):
    return np.array([q["key"] in rag(q["q"], 3, min_overlap).text
                     for q in answerable])


a, b = correct_vector(1), correct_vector(2)
print("overlap>=1", a.sum(), "overlap>=2", b.sum())
rng = np.random.default_rng(0)
diffs = []
for _ in range(2000):
    pick = rng.integers(0, len(a), len(a))
    diffs.append(a[pick].sum() - b[pick].sum())
low, high = np.percentile(diffs, [5, 95])
print("difference", a.sum() - b.sum(), "90% interval", low, high)
print("share of resamples with no gain", np.mean(np.array(diffs) <= 0))
```

```text
overlap>=1 17 overlap>=2 15
difference 2 90% interval 0.0 4.0
share of resamples with no gain 0.1105
```

The difference is 2 questions; but its 90% interval is between 0 and 4, and in
11% of the resamples threshold 1 gives no gain at all. On a set this small it
is not safe to decide on a difference of two questions. On top of that,
threshold 1 gave 5 more wrong answers in 10 (7 against 2). Look at the whole
table instead of a single number, and enlarge the set if the decision matters.

## Evaluating free-text answers

In this section we measured an answer's correctness by whether a phrase appears
in it; that was enough because the example reader returns the source's
sentence as it is. A real model writes the same information in its own words
("valid for three years" instead of "expires after three years"); then phrase
matching can count a correct answer as wrong too. In practice three approaches
are used together:

- **Human evaluation:** the most reliable measure on a small sample.
- **Rule-based checks:** do the numbers, dates and names appear in the source
  (08)?
- **Evaluation with a model:** asking another model to compare the answer with
  the source and the correct answer and give a score. It is fast, but that
  model has its own errors too; its scores are compared with human evaluation
  on a few examples.

## Summary

- RAG is measured piece by piece: retrieval (recall@k, MRR), the answer
  (correct, wrong, missed), abstention (precision, recall).
- Once the place of the error is separated, it is clear what to fix: search for
  retrieval errors, the prompt or the model for reading errors.
- On a small set a difference of a few questions may not mean anything; a
  decision needs more questions.
- The evaluation set is kept fixed; every time the system changes it is
  measured again on the same set.
