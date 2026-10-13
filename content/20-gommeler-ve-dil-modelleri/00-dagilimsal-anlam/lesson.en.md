# Distributional Meaning

In NLP Fundamentals every word was a separate column. "car" and "automobile"
were two columns with no link between them; "cat" was as far from "dog" as
from "bread". In this module we give words **vectors that carry meaning**.
They all start from one idea: **the meaning of a word can be read from the
words around it**. The linguist J. R. Firth summed it up in 1957: "You shall
know a word by the company it keeps." This is called the **distributional
hypothesis**. In this section we see the idea in numbers: we count the
surroundings of a word, build vectors from those counts and measure that
similar words get similar vectors.

## One-hot vectors have no distance

In a bag of words each word was in its own column. Writing a single word
like this gives a **one-hot** vector: 1 in its own column, 0 everywhere
else.

```python
import numpy as np

vocab = ["bread", "cat", "dog"]
one_hot = np.eye(len(vocab))
cat, dog, bread = one_hot[1], one_hot[2], one_hot[0]


def cosine(a, b):
    return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))


print(one_hot)
print(cosine(cat, dog), cosine(cat, bread))
```

```text
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
0.0 0.0
```

The one-hot vectors of two different words are always orthogonal: the cosine
is 0. In this representation "cat" is no closer to "dog" than to "bread". A
model cannot carry what it learns about "cat" over to "dog"; it has to learn
every word from scratch.

## A small world

The data of this module is `corpus_data.py`: simple English sentences built
around animals, food, vehicles, cities and countries, and people (male/
female, royal/young/family). Words of the same class appear in the same
kinds of sentences; here we test whether meaning can be learned from
context.

```python
from collections import Counter

from corpus_data import make_corpus

for sentence in make_corpus(4):
    print(sentence)
sentences = [s.split() for s in make_corpus(20000)]
counts = Counter(w for s in sentences for w in s)
print(len(counts), sum(counts.values()))
print(counts.most_common(5))
```

```text
we ate apple for dinner
we flew to dublin in ireland
the people of madrid love spain
the people of dublin love ireland
166 110308
[('the', 22493), ('in', 3730), ('is', 3528), ('a', 3263), ('and', 2158)]
```

20,000 sentences hold 166 different words and 110,308 tokens. A real
language has hundreds of thousands of words; we keep the world small to see
the idea clearly. The most common word is "the" again.

## The surroundings of a word

The **context** of a word is a fixed number of words around it: with a
**window** of 2, the two words on its left and the two on its right.

```python
def contexts(word, window=2):
    found = Counter()
    for s in sentences:
        for i, w in enumerate(s):
            if w == word:
                left, right = max(0, i - window), min(len(s), i + window + 1)
                found.update(s[j] for j in range(left, right) if j != i)
    return found


for word in ["cat", "dog", "bread"]:
    print(word, contexts(word).most_common(5))
```

```text
cat [('the', 662), ('in', 164), ('and', 160), ('chased', 154), ('a', 94)]
dog [('the', 760), ('and', 211), ('in', 190), ('chased', 164), ('sleep', 95)]
bread [('the', 265), ('and', 191), ('she', 96), ('cooked', 96), ('i', 94)]
```

- "cat" and "dog" appear with the same words: "chased", "the", "and", "in".
  If one replaced the other, the sentences would still make sense.
- The surroundings of "bread" are different: "cooked", "she", "i". The
  context of food is separate from that of animals.
- "the" heads all three. Very frequent words are around every word and
  distinguish nothing; we come back to this below.

## The co-occurrence matrix

Let us write the same count for all words into a table: the row is the word,
the column the context word, the cell how often they appear together. Each
row becomes that word's **vector**.

```python
vocab = sorted(counts)
index = {w: i for i, w in enumerate(vocab)}


def cooccurrence(window):
    M = np.zeros((len(vocab), len(vocab)))
    for s in sentences:
        for i, w in enumerate(s):
            left, right = max(0, i - window), min(len(s), i + window + 1)
            for j in range(left, right):
                if j != i:
                    M[index[w], index[s[j]]] += 1
    return M


def neighbours(M, word, k=5):
    unit = M / np.linalg.norm(M, axis=1, keepdims=True)
    sims = unit @ unit[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


M = cooccurrence(2)
print(M.shape)
for a, b in [("cat", "dog"), ("cat", "bread"), ("cat", "the")]:
    print(a, b, round(cosine(M[index[a]], M[index[b]]), 3))
for word in ["cat", "bread", "car", "paris"]:
    print(word, neighbours(M, word))
```

```text
(166, 166)
cat dog 0.998
cat bread 0.612
cat the 0.193
cat ['cow', 'mouse', 'rabbit', 'dog', 'horse']
bread ['cheese', 'salad', 'cake', 'rice', 'soup']
car ['tram', 'bus', 'truck', 'boat', 'train']
paris ['rome', 'athens', 'lisbon', 'vienna', 'dublin']
```

- Nobody said "a cat is an animal"; we only counted. Still, the nearest
  neighbours of "cat" are other animals, those of "bread" are foods, those of
  "car" vehicles, those of "paris" other capitals.
- "cat" and "dog" are 0.998 similar; but "cat" and "bread" are 0.612 too.
  Most of the counts come from words found everywhere, such as "the", "and",
  "in", and they make the vectors alike. In the next section **PPMI** lowers
  the weight of these words.

## Window size

With a small window only the words right next to it are counted; with a
large one the topic of the sentence comes in too. Let us compare three
windows:

```python
for window in [1, 2, 5]:
    M = cooccurrence(window)
    cat_the = cosine(M[index["cat"]], M[index["the"]])
    print(window, round(cat_the, 3), neighbours(M, "king", 4))
```

```text
1 0.051 ['queen', 'princess', 'uncle', 'man']
2 0.193 ['uncle', 'prince', 'man', 'brother']
5 0.899 ['prince', 'queen', 'uncle', 'man']
```

- As the window grows, "the" looks like everything: its similarity to "cat"
  rises from 0.051 to 0.899. In a wide window frequent words weigh more.
- The neighbours of "king" are people in every window, but their order
  changes. A small window catches more **syntactic** similarity (words that
  can be used in the same place), a large one more **topical** similarity.
  In real applications the window is chosen between 2 and 10 and tried for
  the task.

## Summary

- With one-hot vectors the cosine between two different words is always 0;
  there is no similarity between words.
- The distributional hypothesis: words that appear in similar contexts have
  similar meanings.
- Each row of the co-occurrence matrix is a word vector. Even raw counts
  separate the classes of meaning.
- Frequent words ("the") dominate raw counts and make everything look alike;
  the effect grows with the window. The next section fixes this with PPMI
  and shortens the vectors with SVD.
