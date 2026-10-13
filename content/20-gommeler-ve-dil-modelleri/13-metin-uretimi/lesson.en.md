# Text Generation

A language model gives a probability distribution over the next word at
every step. To generate text we have to **pick a word** from this
distribution, then the next one, then the next. Which word is picked is
decided by the **decoding** method, and the same model produces very
different texts when the method changes. In this section we build a trigram
model from support tickets and try the main methods: greedy choice, beam
search, temperature, the k most likely words and nucleus sampling. Large
language models generate text with the same methods; only the model giving
the probabilities is stronger.

## The model

The unsmoothed form of the trigram model of 06: we count the words that
follow the previous two words and turn them into probabilities. We replace
numbers (`ORD-12345`, `E401`) with `#` so that each number does not become a
separate word.

```python
import math
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z#]+|[.!?,]")


def tokens(text):
    return TOKEN.findall(re.sub(r"\d+", "#", text.lower()))


train = [["<s>", "<s>"] + tokens(t["text"]) + ["</s>"]
         for t in make_tickets(5000, seed=1)]
followers = {}
for s in train:
    for a, b, c in zip(s, s[1:], s[2:]):
        followers.setdefault((a, b), Counter())[c] += 1


def next_probs(a, b):
    counts = followers[a, b]
    total = sum(counts.values())
    return {w: n / total for w, n in counts.items()}


print(len(followers), len(next_probs("<s>", "<s>")))
top = sorted(next_probs("my", "order").items(), key=lambda x: -x[1])[:3]
print([(w, round(p, 3)) for w, p in top])
```

```text
1062 23
[('number', 0.36), ('ord', 0.346), ('history', 0.291)]
```

1062 different two-word histories; 23 options for a ticket's first word.
After "my order" comes "number", "ord" or "history".

## Greedy choice

The simplest way: pick the **most likely** word at every step (greedy
decoding). We also add up the logarithm of the generated sentence's
probability.

```python
def finished(seq, max_len=30):
    return seq[-1] == "</s>" or len(seq) > max_len


def greedy():
    seq, score = ["<s>", "<s>"], 0.0
    while not finished(seq):
        probs = next_probs(seq[-2], seq[-1])
        word = max(probs, key=probs.get)
        score += math.log(probs[word])
        seq.append(word)
    return round(score, 2), " ".join(seq[2:-1])


print(*greedy())
```

```text
-7.46 hey there , the app .
```

- Greedy choice produces the **same** sentence every time: there is no
  randomness.
- The sentence is short and generic. The most likely word at each step does
  not have to give the most likely **sentence**: the choice that looks best
  today can lead down a bad road tomorrow.

## Beam search

**Beam search** carries the best `width` paths together instead of a single
one at each step: it extends every path with all possible words and keeps
the best `width` by total log probability. Finished paths stay in the pool.

```python
import textwrap


def beam_search(width, alpha=0.0):
    beams = [(0.0, ["<s>", "<s>"])]
    while not all(finished(seq) for _, seq in beams):
        pool = []
        for score, seq in beams:
            if finished(seq):
                pool.append((score, seq))
                continue
            for w, p in next_probs(seq[-2], seq[-1]).items():
                pool.append((score + math.log(p), seq + [w]))
        pool.sort(key=lambda c: -c[0] / (len(c[1]) - 2) ** alpha)
        beams = pool[:width]
    score, seq = beams[0]
    return round(score, 2), " ".join(seq[2:-1])


for width in [1, 3, 10, 50]:
    score, text = beam_search(width)
    line = f"{width} {score} {text}"
    print(textwrap.fill(line, 76, subsequent_indent="    "))
```

```text
1 -7.46 hey there , the app .
3 -9.78 hey there , i get error e# when i log in on the app crashes every
    time i open the order page .
10 -9.11 hey there , i get error e# when i log in on the app .
50 -7.27 hello , the parcel arrived damaged and the box was open .
```

- Width 1 is the same as greedy choice. Width 50 found a sentence more likely
  than greedy (−7.27).
- But the progress is not steady: widths 3 and 10 found sentences **less
  likely** than greedy. A narrow beam can prune the start of the greedy path
  in one step and drift somewhere worse. Beam search does not **guarantee**
  finding the most likely sentence; it only searches wider.
- The total log probability goes a little further negative with every word,
  so beam search favours **short** sentences (`alpha`, the first note).

## Sampling and temperature

Chatting models mostly generate not by greedy choice but by **sampling**:
the next word is drawn at random according to the probabilities.
**Temperature** sharpens or flattens the distribution: the probabilities
are reweighted with `p^(1/T)`. `T < 1` strengthens the most likely words,
`T > 1` gives the unlikely words a chance.

There are two more ways to limit the randomness:

- **Top-k**: pick only among the `k` most likely words.
- **Nucleus** (top-p): add up the probabilities from largest to smallest and
  pick from the smallest set of words whose total reaches `p`. When the
  model is sure the set is small; when it is unsure, large.

```python
import random


def sample(rng, temperature=1.0, top_k=None, top_p=None):
    seq, score = ["<s>", "<s>"], 0.0
    while not finished(seq):
        probs = next_probs(seq[-2], seq[-1])
        items = sorted(probs.items(), key=lambda x: -x[1])
        if top_k:
            items = items[:top_k]
        if top_p:
            mass = 0.0
            for i, (w, p) in enumerate(items):
                mass += p
                if mass >= top_p:
                    items = items[:i + 1]
                    break
        words = [w for w, _ in items]
        weights = [p ** (1 / temperature) for _, p in items]
        word = rng.choices(words, weights=weights)[0]
        score += math.log(probs[word])
        seq.append(word)
    return score, " ".join(seq[2:]).replace(" </s>", "")


rng = random.Random(0)
for t in [0.5, 1.0, 2.0]:
    line = f"{t} {sample(rng, temperature=t)[1]}"
    print(textwrap.fill(line, 76, subsequent_indent="    "))
```

```text
0.5 dear support , the parcel arrived damaged and the box was open . how
    long does shipping to prague take ? my package was delivered to the
    wrong amount
1.0 push notifications stopped working after the update . the tracking
    number for ord # ? it has not arrived yet . how long does shipping to
    dublin take ?
2.0 how do i change the email address on my account was locked after too
    many login attempts . regards , gus
```

- With sampling, every run produces a different ticket, and the texts are
  much livelier: city names, names, several sentences.
- But the trigram model only looks two words back: in "my package was
  delivered to the wrong amount", "amount" came after "wrong" instead of an
  address; two separate ticket patterns were stitched together at the seam.
  A stronger model keeps this coherence over long distances.

## Diversity and probability

Let us generate 300 tickets with each setting and measure two things:
**diversity** (distinct-2: the share of different word pairs among all
pairs) and the **log probability per word** the model gives to the generated
text (higher = more "natural" for the model).

```python
def distinct(texts, n):
    grams = [tuple(t.split()[i:i + n]) for t in texts
             for i in range(len(t.split()) - n + 1)]
    return round(len(set(grams)) / len(grams), 3)


settings = {"t=0.5": {"temperature": 0.5}, "t=1.0": {},
            "t=2.0": {"temperature": 2.0}, "k=3": {"top_k": 3},
            "p=0.9": {"top_p": 0.9}}
for name, options in settings.items():
    rng = random.Random(1)
    runs = [sample(rng, **options) for _ in range(300)]
    texts = [text for _, text in runs]
    per_word = sum(s for s, _ in runs) / sum(len(t.split()) + 1 for t in texts)
    print(name, len(set(texts)), distinct(texts, 2), round(per_word, 3))
```

```text
t=0.5 286 0.064 -0.588
t=1.0 298 0.09 -0.666
t=2.0 300 0.131 -0.861
k=3 266 0.051 -0.585
p=0.9 297 0.067 -0.626
```

The columns: the setting, how many of the 300 texts are different,
distinct-2, log probability per word.

- As temperature rises diversity rises (0.064 → 0.131) and probability falls
  (−0.588 → −0.861). This is a **trade-off**: diverse text also contains
  words the model is less sure of; very hot text becomes incoherent.
- The 3 most likely words is the narrowest option: only 266 of the 300
  tickets are different, the lowest diversity.
- Nucleus sampling (p = 0.9) sits between the two ends: it cuts off the tail
  of the distribution and keeps diversity among reasonable words. In large
  language models temperature and nucleus sampling are mostly set together.

## Summary

- The decoding method is how we pick text from the model's probabilities;
  the same model produces very different texts with different methods.
- Greedy choice is deterministic, short and generic. Beam search looks for
  more likely sentences but does not guarantee it, and favours short ones.
- Sampling brings diversity. Temperature, top-k and top-p tune this
  diversity: more diverse text is less likely text for the model.
- For tasks close to a single right answer, such as translation and
  summarising, beam search is preferred; for free text generation,
  sampling.
