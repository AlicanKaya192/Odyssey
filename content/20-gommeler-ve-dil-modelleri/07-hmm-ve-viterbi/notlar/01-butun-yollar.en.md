Is the path Viterbi finds really the best? On a short sentence let us try every
tag sequence one by one and compare. With the lesson's `transition`,
`log_emit`, `tags` and `viterbi`:

```python
from itertools import product


def path_score(sentence, path):
    score, prev = 0.0, START
    for w, t in zip(sentence, path):
        score += transition[prev, index[t]] + log_emit(t, w)
        prev = index[t]
    return score


sentence = "they book the light train".split()
paths = list(product(tags, repeat=len(sentence)))
best = max(paths, key=lambda p: path_score(sentence, p))
print(len(paths), list(best) == viterbi(sentence))
print(list(best))
print(len(sentence) * len(tags) ** 2)
```

```text
16807 True
['PRON', 'VERB', 'DET', 'ADJ', 'NOUN']
245
```

- Five words give 16,807 sequences; the best is the same as Viterbi's.
- Viterbi reaches the same result with `n · T² = 245` comparisons. When the
  number of words doubles, the number of all sequences becomes `7^10 ≈ 282
  million`; Viterbi's work only doubles.
- What makes this possible is the HMM's **Markov assumption**: a tag's score
  depends only on the previous tag. So knowing the best path at one step is
  enough for the next.
