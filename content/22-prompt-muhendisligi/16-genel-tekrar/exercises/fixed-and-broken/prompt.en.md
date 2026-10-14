`compare(old, new, gold)` should compare two versions' answers with the
right answers: wrong in the old and right in the new is fixed, right in the
old and wrong in the new is broken. Return `[fixed, broken, fixed -
broken]`.

**Expected output:**

```
[2, 1, 1]
[0, 0, 0]
```
