`baseline_tags(train, words)` should give each word the tag it got most often
in training (sentences of `[word, tag]` pairs); on ties, the one that comes
first alphabetically. An unseen word gets `"NOUN"`.

**Expected output:**

```
['DET', 'NOUN', 'NOUN']
```
