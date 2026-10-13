A language model is used not only to generate text but also to **judge** it:
which sentence is more natural? With the lesson's bigram model (`logprob`),
let us compare 500 test tickets with their shuffled versions:

```python
import random

rng = random.Random(1)
wins = total = 0
for s in test[:500]:
    words = s[1:-1]
    shuffled = rng.sample(words, len(words))
    if shuffled != words:
        total += 1
        wins += logprob(words) > logprob(shuffled)
print(wins, total)
```

```text
500 500
```

- In 500 of 500 tickets the model found the real order more likely than the
  shuffled one. Even a model that looks only at the previous word knows a lot
  about word order.
- The same idea is used in spelling correction: between "there is my order"
  and "where is my order" a language model says which is more likely. Speech
  recognition too picks, among acoustically similar candidates, the one the
  language model finds more likely.
- Careful: probability shrinks as a sentence gets longer. When comparing
  sentences of different lengths, use not the total log probability but the
  average per word (or perplexity).
