# Recurrent Neural Networks

The network of 08 averaged the word embeddings of a text; the order of the
words was lost and "not bad" looked the same as "bad not". The n-gram
language model of 06 saw order, but only the last word or two. A
**recurrent neural network** (RNN) fills the gap between them: it reads the
text from left to right and updates a **hidden state** at every word. The
hidden state is like a fixed-size summary of what has been read so far:

$$h_t = \tanh(x_t W_x + h_{t-1} W_h + b)$$

The **same** weights are used at every step, so the network can read text of
any length. In this section we build an RNN language model with NumPy, have
it predict the next word, and check whether it sees something the n-gram
model cannot.

## The data

Sentences from the small world; we add `<s>` at the start and `</s>` at the
end of each sentence.

```python
import numpy as np
from corpus_data import make_corpus

sentences = [["<s>"] + s.split() + ["</s>"] for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
seqs = [[index[w] for w in s] for s in sentences]
print(len(vocab), len(seqs), max(len(s) for s in seqs))
print(" ".join(sentences[0]))
```

```text
168 20000 11
<s> we ate apple for dinner </s>
```

168 words, 20,000 sentences; the longest sentence has 11 words (markers
included).

## One step, one sentence

At each step the word's embedding (`E`) and the previous hidden state
combine into the new hidden state; a softmax over the whole vocabulary on the
hidden state gives the probabilities of the next word.

```python
rng = np.random.default_rng(0)
V, D, H = len(vocab), 16, 32
P = {"E": rng.normal(0, 0.1, (V, D)), "Wx": rng.normal(0, 0.1, (D, H)),
     "Wh": rng.normal(0, 0.1, (H, H)), "bh": np.zeros(H),
     "Wo": rng.normal(0, 0.1, (H, V)), "bo": np.zeros(V)}


def forward(seq):
    hs, ps = [np.zeros(H)], []
    for t in range(len(seq) - 1):
        h = np.tanh(P["E"][seq[t]] @ P["Wx"] + hs[-1] @ P["Wh"] + P["bh"])
        z = h @ P["Wo"] + P["bo"]
        p = np.exp(z - z.max())
        hs.append(h)
        ps.append(p / p.sum())
    return hs, ps


hs, ps = forward(seqs[0])
loss = -np.mean([np.log(p[y]) for p, y in zip(ps, seqs[0][1:])])
print(len(hs), hs[1].shape, round(float(ps[0].sum()), 3))
print(round(float(loss), 3), round(float(np.log(V)), 3))
```

```text
7 (32,) 1.0
5.12 5.124
```

- A 7-word sentence gives 6 predictions; `hs` holds 7 states together with
  the zero state at the start. Each hidden state is 32 numbers.
- The untrained network's loss is 5.12, very close to `log 168`: it gives
  roughly equal chances to every word.

## Backpropagation through time

The derivative is computed as in 08, with one difference: a hidden state
affects both that step's prediction and the **later** steps. So we walk the
derivative from the end back to the start, and at each step add the
derivative coming from the next one (`dh_next`). This is called
**backpropagation through time** (BPTT).

```python
def backward(seq):
    hs, ps = forward(seq)
    G = {k: np.zeros_like(v) for k, v in P.items()}
    loss, dh_next = 0.0, np.zeros(H)
    for t in reversed(range(len(seq) - 1)):
        dz = ps[t].copy()
        loss -= np.log(dz[seq[t + 1]])
        dz[seq[t + 1]] -= 1
        G["Wo"] += np.outer(hs[t + 1], dz)
        G["bo"] += dz
        draw = (1 - hs[t + 1] ** 2) * (P["Wo"] @ dz + dh_next)
        G["bh"] += draw
        G["Wx"] += np.outer(P["E"][seq[t]], draw)
        G["Wh"] += np.outer(hs[t], draw)
        G["E"][seq[t]] += P["Wx"] @ draw
        dh_next = P["Wh"] @ draw
    n = len(seq) - 1
    return loss / n, {k: g / n for k, g in G.items()}


for epoch in range(2):
    total = 0.0
    for i in rng.permutation(len(seqs)):
        loss, G = backward(seqs[i])
        total += loss
        norm = np.sqrt(sum((g ** 2).sum() for g in G.values()))
        for k in P:
            P[k] -= 0.2 * min(1.0, 5.0 / norm) * G[k]
    print(epoch, round(total / len(seqs), 3))
```

```text
0 1.352
1 1.156
```

- `1 - h²` is the derivative of `tanh`.
- `min(1.0, 5.0 / norm)` is **gradient clipping**: if the total size of the
  derivatives exceeds 5, they are scaled down. In an RNN the derivative can
  grow by being multiplied across steps (the first note); clipping keeps a
  single bad step from wrecking the weights.
- Two epochs take about 15 seconds on this computer: every sentence is
  processed on its own, word by word. This sequential nature is the RNN's
  biggest weakness.

## Does it remember the pronoun?

In "the queen smiled and ___" the next word should be "she". The answer is
three words back; could the model carry this information in its hidden
state?

```python
from collections import Counter
from corpus_data import GENDER_PAIRS


def next_word_probs(words):
    seq = [index[w] for w in ["<s>"] + words] + [0]
    return forward(seq)[1][-1]


correct = 0
for male, female in GENDER_PAIRS:
    for word, pronoun in [(male, "he"), (female, "she")]:
        p = next_word_probs(["the", word, "smiled", "and"])
        guess = "he" if p[index["he"]] > p[index["she"]] else "she"
        correct += guess == pronoun
print(correct, 2 * len(GENDER_PAIRS))
trigrams = Counter(t for s in sentences for t in zip(s, s[1:], s[2:]))
print(trigrams["smiled", "and", "he"], trigrams["smiled", "and", "she"])
for word in ["queen", "king"]:
    p = next_word_probs(["the", word, "smiled", "and"])
    print(word, round(float(p[index["he"]]), 3), round(float(p[index["she"]]), 3))
```

```text
16 16
316 338
queen 0.029 0.947
king 0.965 0.013
```

- The RNN picks the right pronoun for 16 of 16 person words. After "queen"
  it gives "she" 0.947, after "king" it gives "he" 0.965.
- A trigram model only sees "smiled and": there "she" appeared 338 times,
  "he" 316 times. It always says "she" and gets only 8 of 16. It cannot see
  the subject three words back.
- The RNN learned this without being taught: it carried the "queen"
  information in its hidden state for two steps.

## Generating text

Since a language model gives probabilities, we can also sample from it:
start with `<s>`, pick a word by the probabilities, feed it as input, and
continue until `</s>` comes.

```python
def generate(seed):
    gen = np.random.default_rng(seed)
    h, word, out = np.zeros(H), index["<s>"], []
    while len(out) < 15:
        h = np.tanh(P["E"][word] @ P["Wx"] + h @ P["Wh"] + P["bh"])
        z = h @ P["Wo"] + P["bo"]
        p = np.exp(z - z.max())
        word = gen.choice(V, p=p / p.sum())
        if vocab[word] == "</s>":
            break
        out.append(vocab[word])
    return " ".join(out)


for seed in range(5):
    print(generate(seed))
```

```text
the daughter lives in a small house
the uncle lives in a small house
the dog chased the horse
she is a daughter
we took the bike to berlin
```

All the sentences follow the small world's grammar. On real text an RNN
cannot do this so well; here the world is small and regular. Generation
methods (greedy choice, temperature, the k most likely words) are in section
13.

## Summary

- An RNN reads text from left to right; at each step it updates a hidden
  state with the same weights. The hidden state summarises what was read.
- Training is by backpropagation through time: the derivative walks from the
  end to the start, and each step adds the derivative from the next one.
  Gradient clipping prevents exploding derivatives.
- A small RNN language model chose the pronoun from the subject three words
  back 16/16 right; a trigram that sees only the last two words stayed at
  8/16.
- The RNN's weakness is its sequential nature: each step waits for the
  previous one, and over long distances the derivative can vanish (the first
  note). The attention mechanism of the next section looks at every word in
  a single step.
