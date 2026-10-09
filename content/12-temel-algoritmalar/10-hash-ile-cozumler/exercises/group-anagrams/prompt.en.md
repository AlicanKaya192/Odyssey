Write the function `group_anagrams(words)`: it groups words made of the same
letters and returns the groups as a list. The groups come **in the order their
first word appears in the list**; the words inside a group in input order too.

- `["tea", "eat", "tan", "ate", "nat", "bat"]` →
  `[["tea", "eat", "ate"], ["tan", "nat"], ["bat"]]`

The key: the word's sorted letters (`"".join(sorted(word))`). Since a Python
dictionary keeps insertion order, the order of the groups comes out right by
itself.

**Expected output:**

```
['tea', 'eat', 'ate']
['tan', 'nat']
['bat']
[]
```
