# Evaluation in NLP

In classification evaluation is easy: the prediction is either the right
label or it is not. But if a model **generates text** (a translation, a
summary, an answer), "right" is not a single text: the same thing can be
said with dozens of different sentences. In this section we write the two
most common automatic measures for text generation, **BLEU** and **ROUGE**,
from scratch and look at what they measure and what they miss. Then we turn
to the labels themselves: do two people give the same label to the same
text, and how does this limit evaluation?

## BLEU: the precision of word groups

**BLEU** (Papineni and colleagues, 2002) was developed for machine
translation. It looks at how much of the candidate's 1, 2, 3 and 4-word
groups also appear in the reference (precision). A group is counted at most
as many times as it appears in the reference (clipping); this blocks the
"the the the" trick. The geometric mean of the four precisions is taken, and
candidates shorter than the reference are penalised by a **brevity
penalty**.

```python
import math
from collections import Counter


def ngrams(words, n):
    return Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))


def bleu(candidate, reference, max_n=4):
    c, r = candidate.split(), reference.split()
    logs = []
    for n in range(1, max_n + 1):
        cand, ref = ngrams(c, n), ngrams(r, n)
        clipped = sum(min(k, ref[g]) for g, k in cand.items())
        logs.append(math.log(max(clipped, 1e-9) / max(sum(cand.values()), 1)))
    brevity = min(1.0, math.exp(1 - len(r) / len(c)))
    return round(brevity * math.exp(sum(logs) / max_n), 3)


reference = ("your parcel will arrive on monday and we will send "
             "a tracking number")
candidates = [
    "your parcel will arrive on monday and we will send a tracking number",
    "your parcel will arrive on monday and we will email a tracking code",
    "the package is coming monday , you will get a tracking number by email",
    "your parcel will arrive",
    "the the the the the the the the the the the the",
]
for cand in candidates:
    print(bleu(cand, reference), cand)
```

```text
1.0 your parcel will arrive on monday and we will send a tracking number
0.702 your parcel will arrive on monday and we will email a tracking code
0.001 the package is coming monday , you will get a tracking number by email
0.105 your parcel will arrive
0.0 the the the the the the the the the the the the
```

- The reference itself scores 1.0. The candidate with two changed words
  0.702.
- The third candidate carries **the same meaning** ("package is coming
  monday", the tracking number by email) but scores 0.001 BLEU: the words
  are different and there are almost no shared 3 and 4-word groups. BLEU
  measures the **surface**, not the meaning.
- The short candidate "your parcel will arrive" drops to 0.105 through the
  brevity penalty, even though all its words are right. The repetition trick
  scores 0.
- BLEU is noisy on a single sentence; added up over a whole test set it is
  useful for comparing systems. Using several references helps too (the
  first note).

## ROUGE: recall for summaries

**ROUGE** (Lin, 2004) is common for summaries. Unlike BLEU it looks at
**recall**: how much of the reference summary's word groups are in the
candidate? ROUGE-1 for single words, ROUGE-2 for pairs; **ROUGE-L** looks at
the longest common subsequence, so it also takes word order into account.

```python
def rouge_n(candidate, reference, n):
    cand, ref = ngrams(candidate.split(), n), ngrams(reference.split(), n)
    overlap = sum(min(k, cand[g]) for g, k in ref.items())
    return round(overlap / max(sum(ref.values()), 1), 3)


def lcs(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                table[i + 1][j + 1] = table[i][j] + 1
            else:
                table[i + 1][j + 1] = max(table[i][j + 1], table[i + 1][j])
    return table[-1][-1]


summary = "the parcel arrived damaged and the customer wants a refund"
outputs = ["the customer wants a refund because the parcel arrived damaged",
           "customer parcel damaged refund",
           "the customer wants a new phone and the parcel is fine"]
for out in outputs:
    rouge_l = lcs(out.split(), summary.split()) / len(summary.split())
    print(rouge_n(out, summary, 1), rouge_n(out, summary, 2), round(rouge_l, 3))
```

```text
0.9 0.778 0.5
0.4 0.0 0.3
0.7 0.556 0.4
```

The columns: ROUGE-1, ROUGE-2, ROUGE-L.

- The first candidate is right and fluent; because it swaps the clauses,
  ROUGE-L drops to 0.5, but ROUGE-1 is 0.9.
- The second candidate is four keywords: the core of the meaning is right
  but ROUGE-1 is 0.4.
- The third candidate is **wrong**: the customer wants a new phone and the
  parcel is fine. Still, with ROUGE-1 0.7 and ROUGE-2 0.556 it scores
  **higher** than the keyword list. Shared words ("the customer wants a",
  "the parcel") earn points for a summary whose meaning is reversed.
- The lesson: measures based on word overlap are fast and cheap, but they
  do not measure correctness. Measures based on embedding similarity (as in
  04) catch synonyms; a widely used approach today is to use a strong
  language model as a **judge**. None of them fully replaces human
  evaluation.

## How reliable are the labels?

Human evaluation is not flawless either. Imagine two people labelling 1000
reviews; both are careless on 20% of the reviews and pick a random label.
How well do the two annotators agree? The raw agreement rate is misleading,
because two people can give the same label by chance too. **Cohen's kappa**
subtracts the agreement expected by chance:

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

`p_o` is the observed agreement, `p_e` the chance agreement computed from
the two people's label shares.

```python
import random

from text_data import make_reviews

reviews = make_reviews(1000)
gold = [r["label"] for r in reviews]


def annotator(seed, error):
    rng = random.Random(seed)
    labels = ["positive", "neutral", "negative"]
    return [rng.choice(labels) if rng.random() < error else g for g in gold]


def cohen_kappa(a, b):
    observed = sum(x == y for x, y in zip(a, b)) / len(a)
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[k] * cb[k] for k in ca) / len(a) ** 2
    kappa = (observed - expected) / (1 - expected)
    return round(observed, 3), round(expected, 3), round(kappa, 3)


ann_a, ann_b = annotator(1, 0.2), annotator(2, 0.2)
print(Counter(gold).most_common())
print(*cohen_kappa(ann_a, ann_b))
always = ["positive"] * len(gold)
print(*cohen_kappa(always, gold))
```

```text
[('positive', 671), ('negative', 186), ('neutral', 143)]
0.772 0.442 0.591
0.671 0.671 0.0
```

- The two annotators agree 77.2%; but 44.2% would be expected by chance
  (most reviews are positive). Kappa is 0.591: "moderate" agreement.
- Someone who says "positive" to every review agrees with the true labels
  67.1%; kappa is **0**. All of that agreement comes from the class
  distribution; there is no information in it.
- In real projects an annotation guideline is written, several people label
  the same examples and kappa is measured. If kappa is low, the problem is
  often not the model but the task's definition: even people cannot agree on
  what is "neutral".

## Summary

- BLEU looks at the share of the candidate's word groups found in the
  reference (precision), ROUGE at the share of the reference's word groups
  found in the candidate (recall).
- Both measure the surface: a candidate saying the same thing in different
  words can score low, and a wrong summary sharing words can score high.
- Automatic measures are a cheap start for comparing systems; important
  decisions are backed by human evaluation.
- Cohen's kappa subtracts chance agreement; it shows how reliable the labels
  are and how much we can expect from a model (the second note).
