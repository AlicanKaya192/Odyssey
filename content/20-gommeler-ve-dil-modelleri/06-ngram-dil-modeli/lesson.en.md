# The n-gram Language Model

So far we looked at the meaning of words; now we look at **order**. A
**language model** gives a sequence of words a probability: "where is my
order" is a natural sentence, "order my is where" is not. An equivalent
question: which word comes after these words? Next-word suggestions on your
phone, spelling correction, speech recognition and today's large language
models all answer this question. In this section we build the oldest and
simplest language model, the **n-gram** model, from counts, measure it with
**perplexity** and generate text with it.

## The probability of the next word

The probability of a sentence is, by the chain rule, the product of the
words' conditional probabilities. The n-gram model simplifies this: a word
depends only on the n − 1 words before it. For a bigram (n = 2):

`P(w_i | w_1 ... w_(i−1)) ≈ P(w_i | w_(i−1)) = count(w_(i−1), w_i) / count(w_(i−1))`

Let us try it on the support tickets. We add `<s>` at the start of each
sentence and `</s>` at the end; in the test tickets words never seen in
training become `<unk>`.

```python
import math
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z]+|[.!?]")


def sentences(n, seed):
    return [["<s>"] + TOKEN.findall(t["text"].lower()) + ["</s>"]
            for t in make_tickets(n, seed=seed)]


train = sentences(3000, 1)
vocab = {w for s in train for w in s} | {"<unk>"}
test = [[w if w in vocab else "<unk>" for w in s] for s in sentences(1000, 11)]
bigrams = Counter((a, b) for s in train for a, b in zip(s, s[1:]))
context = Counter(a for s in train for a in s[:-1])
after = {b: n / context["my"] for (a, b), n in bigrams.items() if a == "my"}
print(len(vocab), sum(len(s) for s in train))
print([(w, round(p, 3)) for w, p in sorted(after.items(), key=lambda x: -x[1])[:4]])
```

```text
401 68948
[('account', 0.333), ('order', 0.21), ('card', 0.116), ('package', 0.079)]
```

The most likely words after "my" are "account", "order", "card", "package".
The model learned the patterns of ticket language just by counting.

## The unseen pair problem

The probability of a sentence is a product of small numbers, so we add up
their logarithms. But if the test data has a bigram never seen in training,
its probability is 0 and its logarithm minus infinity:

```python
unseen = sum(1 for s in test for a, b in zip(s, s[1:]) if (a, b) not in bigrams)
print(unseen, sum(len(s) - 1 for s in test))


def p_bigram(a, b, k):
    return (bigrams[a, b] + k) / (context[a] + k * len(vocab))


def logprob(words, k=0.01):
    s = ["<s>"] + words + ["</s>"]
    return sum(math.log(p_bigram(a, b, k)) for a, b in zip(s, s[1:]))


for text in ["where is my order ?", "order my is where ?"]:
    print(text, round(logprob(text.split()), 2))
```

```text
77 22142
where is my order ? -21.92
order my is where ? -52.77
```

- 77 of the 22,142 bigrams are not in training. The probability computed from
  counts (**maximum likelihood**, MLE) gives them 0 and makes the whole
  sentence "impossible".
- The fix is **smoothing**: add a small `k` to every count (**add-k**; with
  `k = 1`, Laplace). An unseen pair gets a small non-zero probability. The
  same idea as the smoothing of Naive Bayes in 08.
- The log probability of the sentence in natural order is −21.9, the
  shuffled one −52.8: the natural order is about `e^31` times more likely.
  The model has learned the order of the language.

## Perplexity

The usual way to measure a language model on test data is **perplexity**:
`e` raised to minus the average log probability given to the test words.

`PPL = exp( −(1/N) Σ log P(w_i | history) )`

The intuition: among how many words, on average, is the model **undecided**
at each step? Lower perplexity means a better model.

```python
N = sum(len(s) - 1 for s in test)


def perplexity(prob):
    total = 0.0
    for s in test:
        for i in range(1, len(s)):
            p = prob(s, i)
            if p == 0:
                return math.inf
            total += math.log(p)
    return round(math.exp(-total / N), 2)


unigrams = Counter(w for s in train for w in s[1:])
n_uni = sum(unigrams.values())
print("unigram", perplexity(lambda s, i: (unigrams[s[i]] + 1) / (n_uni + len(vocab))))
print("bigram mle", perplexity(lambda s, i: p_bigram(s[i - 1], s[i], 0)))
for k in [1, 0.1, 0.01]:
    print("bigram", k, perplexity(lambda s, i: p_bigram(s[i - 1], s[i], k)))
```

```text
unigram 97.77
bigram mle inf
bigram 1 7.01
bigram 0.1 4.18
bigram 0.01 3.79
```

- The unigram model (which knows no order at all) gets 97.8: as if undecided
  among about 98 words at each step.
- The bigram from counts (MLE) is infinite: a single unseen pair is enough.
- Add-1 (Laplace) gives 7.01, add-0.01 gives 3.79. `k = 1` is too much: it
  hands too much probability to unseen pairs, stealing it from the seen ones.
  `k` is a setting; it is chosen on validation data.

## A longer history: the trigram

```python
trigrams = Counter((a, b, c) for s in train for a, b, c in zip(s, s[1:], s[2:]))
pairs = Counter((a, b) for s in train for a, b in zip(s[:-1], s[1:-1]))


def p_trigram(s, i, k):
    if i == 1:
        return p_bigram(s[0], s[1], k)
    a, b, c = s[i - 2], s[i - 1], s[i]
    return (trigrams[a, b, c] + k) / (pairs[a, b] + k * len(vocab))


for k in [0.1, 0.01, 0.001]:
    print("trigram", k, perplexity(lambda s, i: p_trigram(s, i, k)))
```

```text
trigram 0.1 2.73
trigram 0.01 2.2
trigram 0.001 2.15
```

A two-word history lowers perplexity from 3.79 to 2.15. A longer history
means better prediction; but as n grows the number of unseen n-grams
explodes (the vocabulary explosion of 04) and the count tables become huge.
This is the limit of n-gram models: the history can only be a few words.

## Generating text

A language model can **sample** as well as give probabilities: start from
`<s>`, draw the next word by its probability, continue until `</s>` comes.

```python
import random
import textwrap

followers = {}
for (a, b, c), n in trigrams.items():
    followers.setdefault((a, b), []).append((c, n))
rng = random.Random(0)
for _ in range(3):
    history, out = ("<s>", rng.choice([b for (a, b) in pairs if a == "<s>"])), []
    out.append(history[1])
    while history[1] != "</s>" and len(out) < 25:
        words, weights = zip(*followers[history])
        nxt = rng.choices(words, weights=weights)[0]
        out.append(nxt)
        history = (history[1], nxt)
    text = " ".join(w for w in out if w != "</s>")
    print(textwrap.fill(text, 76, subsequent_indent="  "))
```

```text
my invoice for order ord ? why did my card .
please reset the password for hana example . com . my account . my order
  number is ord . this is urgent !
good morning can i change the delivery address for order ord ? i used the
  mobile app . please help .
```

The generated tickets are fluent word by word but can be inconsistent as a
whole ("my invoice for order ord ? why did my card ."): the model looks only
at the last two words. (Since the tokeniser keeps only letters, order numbers
became "ord" and emails "hana example . com".) It does not remember at the
end of a sentence what was said at its start. For models that can carry a
long history we turn to neural networks.

## Summary

- The n-gram language model estimates the probability of the next word from
  the previous n − 1 words, by counting.
- An unseen n-gram makes the probability 0 under MLE; add-k smoothing
  prevents this, and `k` is tuned.
- Perplexity is the average "indecision" on test data: unigram 97.8, bigram
  3.79, trigram 2.15.
- An n-gram model can generate text but sees only a history of a few words.
