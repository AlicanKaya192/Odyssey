# Working with Embeddings

We learned two ways of building word vectors. This section is about **using**
them: writing them to a file and reading them back, meeting a word that is
not in the vocabulary, finding the nearest neighbours fast. Then we look at
the most important trap of embeddings: **bias**. Embeddings learn the
patterns of the text they are trained on; if the text always says "she"
after "nurse", the vector carries that too. We will measure this bias, try to
remove it and see why removing it is not easy.

In this section we add 4000 sentences about occupations (`make_jobs`) to the
corpus. These sentences are biased on purpose: in 85% of the "nurse"
sentences the pronoun is "she", in 85% of the "engineer" sentences "he". To
catch the bias clearly we chose a window of 3 and 50 dimensions.

## Saving and reading vectors

Trained embeddings are usually shared as plain text: on each line the word
and its numbers. Real ready-made embedding files mostly use this format too.

```python
import numpy as np
from corpus_data import JOB_SKEW, GENDER_PAIRS, make_corpus, make_jobs

sentences = [s.split() for s in make_corpus(20000) + make_jobs(4000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    for i, w in enumerate(s):
        for j in range(max(0, i - 3), min(len(s), i + 4)):
            if j != i:
                M[index[w], index[s[j]]] += 1
with np.errstate(divide="ignore"):
    P = np.maximum(np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0))), 0)
U, S, _ = np.linalg.svd(P)
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)

with open("vectors.txt", "w", encoding="utf-8") as f:
    for word in vocab:
        f.write(word + " " + " ".join(f"{x:.4f}" for x in E[index[word]]) + "\n")
loaded = {}
with open("vectors.txt", encoding="utf-8") as f:
    for line in f:
        word, *numbers = line.split()
        loaded[word] = np.array(numbers, dtype=float)
print(len(loaded), len(loaded["cat"]))
print(round(float(np.abs(loaded["cat"] - E[index["cat"]]).max()), 5))
```

```text
185 50
5e-05
```

- 185 words, 50 numbers each. Since we rounded to four places, the vector we
  read differs from the original by at most 0.00005; negligible for
  similarity.
- `word, *numbers = line.split()` puts the first part of the line into the
  word and the rest into a list.
- For large embedding files (hundreds of thousands of words × 300 numbers)
  the text format is slow to read; then a binary format with `np.save` and a
  separate word list is used.

## A word not in the vocabulary

An embedding table knows only the words seen in training. When a new word
arrives, a decision is needed:

```python
def vector(word):
    return loaded.get(word)


sentence = "the cat ate pizza".split()
known = [w for w in sentence if vector(w) is not None]
print(known, [w for w in sentence if w not in known])
average = np.mean([vector(w) for w in known], axis=0)
print(average.shape)
```

```text
['the', 'cat', 'ate'] ['pizza']
(50,)
```

- "pizza" never appeared in training: it has no vector. Here we skipped it
  and took the average of the known words (the topic of the next section: a
  document vector).
- Other options: give it a zero vector, or learn an "unknown" (UNK) vector.
  The lasting fix is subword pieces: even if "pizza" is unknown, "piz" and
  "za" may be known. We will see this in the BPE section.

## Finding the nearest neighbours fast

To find neighbours we computed all the similarities and sorted them. If only
the first k are needed, sorting everything is wasteful: `np.argpartition`
finds the k largest, unordered, in linear time; then only those k are
sorted.

```python
sims = E @ E[index["cat"]]
top = np.argpartition(-sims, 5)[:5]
top = top[np.argsort(-sims[top])]
print([vocab[i] for i in top])
print([vocab[i] for i in np.argsort(-sims)[:5]])
```

```text
['cat', 'cow', 'mouse', 'horse', 'rabbit']
['cat', 'cow', 'mouse', 'horse', 'rabbit']
```

Both ways give the same result ("cat" itself comes first). With 185 words
the difference is not felt; in an embedding table of a million words,
finding k items instead of sorting the whole array is clearly faster. Very
large tables use approximate nearest neighbour (ANN) methods; the LSH you saw
in section 13 is one of them.

## Measuring bias

Let us find a **direction** that carries the gender relation: the average of
the differences of female and male word pairs ("woman − man", "queen −
king", "she − he"...). A word's projection onto this direction (the dot
product) says how far it sits on the "female" or "male" side.

```python
pairs = GENDER_PAIRS + [("he", "she"), ("his", "her")]
gender = np.mean([E[index[f]] - E[index[m]] for m, f in pairs], axis=0)
gender = gender / np.linalg.norm(gender)
jobs = list(JOB_SKEW)
projection = np.array([E[index[j]] @ gender for j in jobs])
for job, p in zip(jobs, projection):
    print(f"{job:<10} {JOB_SKEW[job]:.2f} {p:+.3f}")
skew = np.array([JOB_SKEW[j] for j in jobs])
print(round(float(np.corrcoef(projection, skew)[0, 1]), 3))
```

```text
nurse      0.85 +0.167
secretary  0.85 +0.137
dancer     0.80 +0.131
florist    0.80 +0.151
engineer   0.15 -0.227
pilot      0.15 -0.229
mechanic   0.20 -0.231
plumber    0.20 -0.217
teacher    0.50 -0.046
writer     0.50 -0.055
0.997
```

- Occupations with a high share of "she" in the data are on the positive
  side, those with a low share on the negative side; the half-and-half ones
  (teacher, writer) are near the middle.
- The correlation is 0.997: the vectors copied the bias of the data almost
  exactly. The model never tried to learn "nursing is women's work"; it only
  counted which words appear together.

## Biased analogies

Let us ask analogies among occupations only:

```python
def analogy(E, a, b, c, candidates):
    sims = E @ (E[index[b]] - E[index[a]] + E[index[c]])
    return max(candidates, key=lambda w: -np.inf if w in (a, b, c) else sims[index[w]])


print(analogy(E, "man", "engineer", "woman", jobs))
print(analogy(E, "he", "pilot", "she", jobs))
print(analogy(E, "she", "nurse", "he", jobs))
```

```text
florist
engineer
secretary
```

The answer to "man : engineer :: woman : ?" is "florist". Similar results
were published for real embeddings (Bolukbasi and colleagues, 2016: "man :
computer programmer :: woman : homemaker"). A system built on such vectors,
for example a search that ranks CVs, can carry the bias into its decisions.

In the other two questions the answers are "engineer" and "secretary": the
analogy calculation often slides to the nearest neighbour of the question
word ("pilot", "nurse"). This is a known weakness of the analogy test; do not
decide by looking at a single analogy.

## Trying to remove the bias

The best-known method is to **neutralize**: remove the component along the
gender direction from the vectors of words that should have nothing to do
with gender.

```python
D = E.copy()
for job in jobs:
    v = D[index[job]] - (D[index[job]] @ gender) * gender
    D[index[job]] = v / np.linalg.norm(v)
print(round(float(max(abs(D[index[j]] @ gender) for j in jobs)), 6))
print(analogy(D, "man", "engineer", "woman", jobs))


def job_neighbours(E, word):
    sims = {j: E[index[word]] @ E[index[j]] for j in jobs if j != word}
    return sorted(sims, key=sims.get, reverse=True)[:3]


print(job_neighbours(E, "nurse"), job_neighbours(D, "nurse"))
```

```text
0.0
florist
['secretary', 'dancer', 'florist'] ['secretary', 'dancer', 'florist']
```

- The projection is now zero: the bias we measured has been "removed".
- But the analogy is still "florist", and the nearest occupations of "nurse"
  are still the other "female" occupations. The bias is not in a single
  direction; it is also in how the occupations are arranged relative to each
  other. Gonen and Goldberg (2019) showed this with real embeddings and
  called this kind of removal "lipstick on a pig".
- The lesson: setting a single measure of bias to zero does not remove it.
  In a system that decides with embeddings, bias must be measured on the
  system's **decisions**, and the data itself must be reviewed.

## Summary

- Embeddings are stored as "word numbers" per line; binary formats for large
  tables.
- A word not in the vocabulary needs a decision: skip it, give it zeros, a
  UNK vector, or subword pieces.
- For the first k neighbours `np.argpartition` is faster than a full sort.
- Embeddings carry the bias of the data: a correlation of 0.997 between the
  projection and the share in the data. Neutralizing zeroes the measure but
  does not fix the analogies or the neighbourhoods.
