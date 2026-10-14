`remember(memory, text)` should update and return **a copy** of the memory
(do not change the given dictionary): for each of the given `FACTS`
patterns that matches, the value is the last group if the pattern has
one, otherwise the whole match (`found.group(found.lastindex or 0)`).
Leave keys that do not match alone.

**Expected output:**

```
{'name': 'Ada'}
{'name': 'Ada', 'order': 'ORD-48213'}
{'name': 'Ada', 'order': 'ORD-48213'}
```
