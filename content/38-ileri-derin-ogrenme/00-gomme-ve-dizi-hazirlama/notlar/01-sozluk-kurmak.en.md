In the lesson we put every word of the text into the vocabulary. With real
data this causes two problems: the vocabulary grows very large (every typo
becomes a separate word), and because `<unk>` never appears in training the
network never learns that vector. The common fix: put only words that appear
at least a few times into the vocabulary and treat the rest as `<unk>`.

```python
from collections import Counter
from dl_data import TEXT

sentences = [s.split() for s in TEXT.split(".") if s.strip()]
counts = Counter(w for s in sentences for w in s)
kept = sorted(w for w, c in counts.items() if c >= 2)
vocab = ["<pad>", "<unk>"] + kept
index = {w: i for i, w in enumerate(vocab)}
print(len(counts), len(kept), len(vocab))

new = "the fox sat on the warm mat".split()
ids = [index.get(w, 1) for w in new]
print(ids)
print(sum(i == 1 for i in ids))
```

```text
24 15 17
[13, 1, 10, 8, 13, 1, 1]
3
```

- Of 24 different words, 15 appear at least twice;
  with the special tokens the vocabulary has 17 words.
- In the new sentence "fox" had never appeared, and "warm" and "mat"
  appeared only once, so they did not enter the vocabulary: three words
  became `<unk>`.

## Rules

| Rule | Why |
|---|---|
| Build the vocabulary from the training data only | If test words leak into the vocabulary, the score is measured too optimistically |
| `<pad>` is 0, `<unk>` is 1 | `padding_idx=0` and `index.get(w, 1)` always stay the same |
| Treat rare words as `<unk>` | The network learns the `<unk>` vector too and the vocabulary shrinks |
| Save the vocabulary with the model | A vocabulary built in another order gives other ids, and the model reads the wrong rows |

The last rule is the one most often forgotten: without `sorted` the order of
the set could change between runs, and a saved model would give meaningless
results with the new vocabulary.
