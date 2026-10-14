`store_all(texts)` should decide for each text whether to store it: if the
given `SECRET` pattern is found in the text, `"not stored"` (nothing is
taken from that text), otherwise `"stored"` and add all order numbers in
the text (`ORDER.findall`) to the list. Return `[decisions, order
numbers]`.

**Expected output:**

```
stored
not stored
not stored
stored
['ORD-48213', 'ORD-23345', 'ORD-55102']
```
