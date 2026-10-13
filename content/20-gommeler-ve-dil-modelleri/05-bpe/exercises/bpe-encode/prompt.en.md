`encode(word, merges)` should split the word into letters, add `"</w>"` and
apply the rules in the `merges` list **in order**. `merge_pair` is ready.

**Expected output:**

```
['low', 'er</w>']
['s', 'low', '</w>']
```
