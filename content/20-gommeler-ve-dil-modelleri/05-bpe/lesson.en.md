# Subword Tokenisation: BPE

Every word-level method has the same problem: the **out-of-vocabulary** (OOV)
word. A word never seen in training has no count, no TF-IDF column, no
vector. Going down to characters solves this (every word is made of
characters) but makes sequences very long. **BPE** (byte pair encoding)
finds a way between the two: frequent words stay in one piece, rare words are
split into meaningful **subword** pieces. Almost all of today's large
language models work on text split with BPE or a very similar method. In
this section we write BPE from scratch.

## Out-of-vocabulary words

Let us build a word vocabulary from 5000 tickets and see how many words in
2000 new tickets are not in it:

```python
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z]+")
train = Counter(w for t in make_tickets(5000, seed=1)
                for w in TOKEN.findall(t["text"].lower()))
test = Counter(w for t in make_tickets(2000)
               for w in TOKEN.findall(t["text"].lower()))
unseen = {w: n for w, n in test.items() if w not in train}
print(len(train), len(unseen), sum(unseen.values()), sum(test.values()))
print(sorted(unseen, key=unseen.get, reverse=True)[:5])
```

```text
429 16 19 36716
['notificaitons', 'cusotmer', 'stopepd', 'ocotber', 'shippnig']
```

- Only 19 of 36,716 words are out of the vocabulary; but these 16 different
  words are all typos: "notificaitons", "cusotmer"... There is no end to
  typos; every new text brings new ones.
- In real language out-of-vocabulary words are far more common: names, new
  products, foreign words, inflected forms in languages such as Turkish.

## Learning BPE

The idea of BPE comes from a compression method (Gage, 1994) and was brought
to NLP by Sennrich and colleagues (2016):

1. Split each word into its characters; add an end-of-word mark `</w>`.
2. Count the pairs of adjacent symbols in all words (weighted by the word's
   frequency).
3. Merge the most frequent pair into a single symbol; this is a **merge
   rule**.
4. Go back to 2 until you have the number of rules you want.

```python
def pair_counts(words):
    pairs = Counter()
    for symbols, n in words.items():
        for a, b in zip(symbols, symbols[1:]):
            pairs[a, b] += n
    return pairs


def merge(symbols, pair):
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def learn_bpe(counts, n_merges):
    words = {tuple(w) + ("</w>",): n for w, n in counts.items()}
    merges = []
    for _ in range(n_merges):
        pairs = pair_counts(words)
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))
        merges.append(best)
        new_words = Counter()
        for symbols, n in words.items():
            new_words[merge(symbols, best)] += n
        words = new_words
    return merges


merges = learn_bpe(train, 300)
print(merges[:4])
print(merges[4:8])
```

```text
[('e', '</w>'), ('s', '</w>'), ('d', '</w>'), ('o', 'r')]
[('t', 'h'), ('t', '</w>'), ('e', 'r'), ('y', '</w>')]
```

- The first rules are word endings: `e</w>`, `s</w>`, `d</w>`. In English the
  most frequent letter pairs are at the ends of words.
- Then `or`, `th`, `er`. Later rules join these pieces (`th` + `e</w>` =
  "the"), building longer, meaningful pieces step by step.
- On pairs with equal counts the key `(count, pair)` makes the result
  deterministic; every run gives the same rules.

## Splitting a new word

A new word is split into characters and the learned rules are applied **in
the order they were learned**:

```python
def encode(word, merges):
    symbols = tuple(word) + ("</w>",)
    for pair in merges:
        symbols = merge(symbols, pair)
    return list(symbols)


for word in ["refund", "refunded", "parcel", "pracel", "zebra"]:
    print(word, encode(word, merges))
```

```text
refund ['refund</w>']
refunded ['refun', 'd', 'ed</w>']
parcel ['parcel</w>']
pracel ['p', 'r', 'ac', 'e', 'l</w>']
zebra ['z', 'e', 'b', 'r', 'a</w>']
```

- "refund" and "parcel" are frequent words: one piece each.
- "refunded" was rare in training: `refun + d + ed</w>`. Still, it has
  meaningful pieces; a model can reuse here what it learned for the "refun"
  piece. (`refund` + `ed` would be nicer; BPE knows no grammar, it only
  counts.)
- The misspelled "pracel" was split into pieces too: `p + r + ac + e + l</w>`.
- "zebra" never appeared in the tickets: it was split down to its letters.
  But **no word is ever out of the vocabulary**: at worst it is written with
  letters.
- Thanks to the end-of-word mark the pieces can be joined back: put a space
  wherever you see `</w>`.

## How many rules?

The number of rules is a setting: few rules give a short vocabulary but long
sequences, many rules the opposite.

```python
def symbols_used(counts, merges):
    return {s for w in counts for s in encode(w, merges)}


for n in [0, 50, 100, 300, 1000]:
    m = learn_bpe(train, n)
    tokens = sum(len(encode(w, m)) * c for w, c in test.items())
    print(n, len(symbols_used(train, m)), round(tokens / sum(test.values()), 2))
```

```text
0 26 5.08
50 75 2.95
100 121 2.38
300 277 1.34
1000 468 1.0
```

- 0 rules, i.e. character level: 26 symbols but 5.08 pieces per word.
- With 300 rules, 1.34 pieces per word; most words are one piece, rare ones
  are split.
- At 1000 rules almost every word is down to one piece (1.0); now very close
  to word level. Real models usually choose a vocabulary between 30,000 and
  100,000 pieces.

## Summary

- At word level out-of-vocabulary words are unavoidable; character level
  makes sequences long.
- BPE learns a vocabulary of pieces by repeatedly merging the most frequent
  pair of symbols; frequent words are one piece, rare ones are split into
  subwords.
- A new word is split by applying the rules in the order they were learned;
  no word is ever out of the vocabulary.
- The number of rules is a trade-off between vocabulary size and sequence
  length.
