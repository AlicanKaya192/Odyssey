`check(text, rules)` should return the names of the rules the answer
fails, as a list in this order: `max_words`, `max_sentences`,
`must_include`, `must_not_include`. A rule missing from the dictionary is
not checked. Sentences are split with `re.split(r"[.!?]+", text)` and
empty pieces are not counted; `must_include` ignores case,
`must_not_include` does not.

**Expected output:**

```
ok
['max_sentences', 'must_not_include']
['must_include']
```
