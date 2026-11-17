`encode(sentence, vocab)` should turn a list of words into ids. A word's id
is its position in the `vocab` list; a word not in the vocabulary gets `1`,
the id of `<unk>`.

**Expected output:**

```
[4, 2, 3]
[4, 1, 1]
```
