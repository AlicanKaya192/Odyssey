How well does a pretrained model know your text? `coverage(vocab, texts)`
should lowercase the texts, split them on spaces, and return the share of
words that are in the `vocab` set with 3 places. If there are no words,
`0.0`.

**Expected output:**

```
0.5
0.0
```
