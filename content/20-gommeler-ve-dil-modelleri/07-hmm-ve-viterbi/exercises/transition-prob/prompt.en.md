`transition_prob(train, a, b)` should put `"<s>"` before each sentence's tags
and return `P(b | a) = count(a, b) / count(a followed by a tag)` with 3
places (`0.0` if `a` was never seen).

**Expected output:**

```
0.5
1.0
0.0
```
