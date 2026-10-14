`check_citations(answer, sources)` should split the answer into sentences
with `". "`. In every sentence it looks for a source number of the form `[n]`
(`n` starts at 1). A sentence is valid, `True`, if there is a number,
`1 <= n <= len(sources)`, and every number in the sentence (`r"\d+"`;
excluding the source number itself) appears as a number in `sources[n - 1]`.
Return a list of `True`/`False` per sentence.

**Expected output:**

```
[True, False, False]
```
