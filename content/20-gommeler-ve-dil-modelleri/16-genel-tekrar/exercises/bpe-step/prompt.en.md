`bpe_step(words)` should find the most frequent adjacent pair in words made of
symbol lists (on ties, the pair first in alphabetical order) and merge its
occurrences into one symbol in every word, left to right. If there are no
pairs, return the words unchanged.

**Expected output:**

```
['lo w', 'lo w e r', 'n e w']
['low', 'low e r', 'n e w']
```
