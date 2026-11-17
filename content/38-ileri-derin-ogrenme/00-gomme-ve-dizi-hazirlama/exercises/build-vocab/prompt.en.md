`build_vocab(sentences, min_count)` should build a vocabulary from lists of
words: first `"<pad>"` and `"<unk>"`, then the words that appear at least
`min_count` times, **in alphabetical order**. Return the vocabulary as a
list.

**Expected output:**

```
7
['<pad>', '<unk>', 'cat', 'the']
```
