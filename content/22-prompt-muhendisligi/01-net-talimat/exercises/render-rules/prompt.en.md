`render_rules(rules)` should write a line for each rule **present** in the
dictionary and skip the missing ones. The order and form are as in the
lesson:

- `max_words` → `Words: at most N.`
- `max_sentences` → `Sentences: at most N.`
- `must_include` → `Mention: a, b.`
- `must_not_include` → `Do not use: x y`

Join the lines with `"\n"` and return them.

**Expected output:**

```
Words: at most 15.
Mention: tent, zip.
---
Sentences: at most 2.
```
