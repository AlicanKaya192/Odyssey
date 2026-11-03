`escape_like(term)` should put a `\` in front of the `\`, `%` and
`_` characters in the text. The starter code escapes the right characters
but in the **wrong order**: because it escapes `\` last, it also doubles
the escape marks it has just added. First `\`, then `%` and `_`.

**Expected output:**

```
0% ['50% discount']
_ ['plan_b']
n_b ['plan_b']
```
