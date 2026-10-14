`verify(answer, sources)` should write the lesson's verification. If the
answer is `NOT_FOUND`, `True`. Otherwise there must be a source number of the
form `[n]`, `1 <= n <= len(sources)` must hold, and the answer's numbers
(excluding the source number itself) must be among the numbers of
`sources[n - 1]`; otherwise `False`.

**Expected output:**

```
True
False
False
```
