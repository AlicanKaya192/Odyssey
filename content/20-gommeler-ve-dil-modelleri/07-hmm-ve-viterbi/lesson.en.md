# Part-of-Speech Tagging with HMMs

In section 14 of NLP Fundamentals we saw that information extraction turns
into a **sequence labelling** problem: one label per token. In this section
we solve a classic sequence labelling task, **part-of-speech tagging**:
finding whether each word is a noun, a verb or an adjective. The difficulty:
"book" can be a noun ("the book") or a verb ("I book a table"); the decision
depends on the **neighbours**. For this we build a **hidden Markov model**
(HMM) and find the most likely tag sequence with the **Viterbi** algorithm.

## The data: tagged sentences

`make_tagged` generates sentences with every word tagged. The tags: DET
(determiner: the, a), NOUN, VERB, ADJ (adjective), ADP (preposition), PRON
(pronoun), ADV (adverb).

```python
import math
from collections import Counter

import numpy as np
from corpus_data import make_tagged

train = make_tagged(3000)
test = make_tagged(1000, seed=14)
print(" ".join(f"{w}/{t}" for w, t in train[0]))
tags = sorted({t for s in train for _, t in s})
pairs = Counter((w, t) for s in train for w, t in s)
options = {}
for w, t in pairs:
    options.setdefault(w, set()).add(t)
print(tags)
for w, ts in sorted(options.items()):
    if len(ts) > 1:
        print(w, sorted(ts))
```

```text
you/PRON today/ADV light/VERB a/DET quiet/ADJ park/NOUN
['ADJ', 'ADP', 'ADV', 'DET', 'NOUN', 'PRON', 'VERB']
book ['NOUN', 'VERB']
light ['ADJ', 'NOUN', 'VERB']
park ['NOUN', 'VERB']
run ['NOUN', 'VERB']
train ['NOUN', 'VERB']
watch ['NOUN', 'VERB']
```

Six words have more than one tag: "book", "park", "run", "train", "watch"
can be nouns or verbs; "light" can even be any of three ("a light bag", "the
light", "we light the fire").

## Baseline: the most frequent tag

The simplest tagger gives each word the tag it got most often in training:

```python
best = {w: max(ts, key=lambda t: pairs[w, t]) for w, ts in options.items()}
words = [(w, t) for s in test for w, t in s]
hits = [best[w] == t for w, t in words]
ambiguous = [best[w] == t for w, t in words if len(options[w]) > 1]
print(round(sum(hits) / len(hits), 3), round(sum(ambiguous) / len(ambiguous), 3))
```

```text
0.914 0.619
```

- Overall accuracy is 91.4%, but only 61.9% on ambiguous words: "book" gets
  the same tag everywhere.
- The right tag of an ambiguous word comes from its surroundings: after
  "the" comes a noun, after "i" a verb. The model must know this.

## The hidden Markov model

An HMM knows two things:

- **Transition probabilities** `P(tag | previous tag)`: after DET mostly ADJ
  or NOUN come, after PRON a VERB. The tags form a Markov chain.
- **Emission probabilities** `P(word | tag)`: how often does the NOUN tag
  "produce" "book"?

The tags are **hidden**; we only see the words. The model thinks "first a tag
is chosen, then that tag produces a word". Let us estimate both from counts,
with smoothing:

```python
START = len(tags)
index = {t: i for i, t in enumerate(tags)}
transition = np.ones((len(tags) + 1, len(tags)))
emission = {t: Counter() for t in tags}
for s in train:
    prev = START
    for w, t in s:
        transition[prev, index[t]] += 1
        emission[t][w] += 1
        prev = index[t]
transition = np.log(transition / transition.sum(axis=1, keepdims=True))
V = len(options) + 1


def log_emit(t, w):
    total = sum(emission[t].values())
    return math.log((emission[t][w] + 0.01) / (total + 0.01 * V))


for a, b in [("DET", "NOUN"), ("DET", "VERB"), ("PRON", "VERB")]:
    print(a, b, round(math.exp(transition[index[a], index[b]]), 3))
for t in ["NOUN", "VERB"]:
    print(t, round(math.exp(log_emit(t, "book")), 3))
```

```text
DET NOUN 0.665
DET VERB 0.0
PRON VERB 0.667
NOUN 0.109
VERB 0.056
```

- After DET, NOUN is likely and VERB almost never comes. After PRON mostly
  VERB.
- "book" is emitted by both NOUN and VERB. The transition probabilities will
  decide which one is chosen.
- The `START` row holds the probabilities of a sentence's first tag.
  Transitions are smoothed with +1 (Laplace), emissions with +0.01; unseen
  words get a small probability too.

## Viterbi: the most likely tag sequence

In a sentence of 6 words with 7 tags there are `7^6 = 117,649` possible tag
sequences; trying them all becomes impossible for long sentences. The
**Viterbi** algorithm uses dynamic programming (the Algorithm Techniques
module): at each step, for each tag, it keeps the **best** path reaching that
tag and drops the rest.

```python
def viterbi(sentence):
    n, T = len(sentence), len(tags)
    score = np.full((n, T), -np.inf)
    back = np.zeros((n, T), dtype=int)
    for j, t in enumerate(tags):
        score[0, j] = transition[START, j] + log_emit(t, sentence[0])
    for i in range(1, n):
        for j, t in enumerate(tags):
            candidates = score[i - 1] + transition[:T, j]
            back[i, j] = int(np.argmax(candidates))
            score[i, j] = candidates[back[i, j]] + log_emit(t, sentence[i])
    path = [int(np.argmax(score[-1]))]
    for i in range(n - 1, 0, -1):
        path.append(int(back[i, path[-1]]))
    return [tags[j] for j in reversed(path)]


for text in ["i book a table", "the book was long", "we light the old watch"]:
    print(text, viterbi(text.split()))
```

```text
i book a table ['PRON', 'VERB', 'DET', 'NOUN']
the book was long ['DET', 'NOUN', 'VERB', 'ADJ']
we light the old watch ['PRON', 'VERB', 'DET', 'ADJ', 'NOUN']
```

- "i book a table": "book" is a verb; "the book was long": a noun. The same
  word, two different tags depending on the neighbours.
- "we light the old watch": "light" is a verb, "watch" a noun. At each step
  only T × T comparisons are made: the total work is `n · T²`, not `T^n`.
- The `back` table stores in each cell "which tag we came from"; following it
  from the end back to the start gives the best path.

## Measuring

```python
correct = ambiguous_correct = ambiguous_total = 0
for s in test:
    predicted = viterbi([w for w, _ in s])
    for (w, t), p in zip(s, predicted):
        correct += p == t
        if len(options[w]) > 1:
            ambiguous_total += 1
            ambiguous_correct += p == t
print(round(correct / len(words), 3), round(ambiguous_correct / ambiguous_total, 3))
```

```text
0.995 0.976
```

On ambiguous words accuracy rose from 61.9% to 97.6%, overall from 91.4% to
99.5%. The word itself was not enough; the **order** of the tags (the
transition probabilities) filled in the missing information.

## Summary

- Part-of-speech tagging is a sequence labelling task; the tag of an
  ambiguous word depends on its neighbours.
- An HMM treats tags as a hidden Markov chain: transitions `P(tag |
  previous)`, emissions `P(word | tag)`. Both from counts.
- Viterbi finds the most likely tag sequence with dynamic programming in
  `n · T²` work.
- The most-frequent-tag baseline scores 91.4%, the HMM 99.5%; on ambiguous
  words from 61.9% to 97.6%.
