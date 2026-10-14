The read-only `tiny_chat.py` holds the lesson's toy model (`ask`,
`CAPITALS`). `audit(countries)` should ask every country with
`ask(country)`. The answer has the form `"the capital of X is Y ."`: `X` is
the answer's country, `Y` its capital. Return three numbers:
`[correct, wrong capital, other country]`. It is correct if the capital is
`CAPITALS[country]`; otherwise, if the answer's country is not the asked
country, it is "other country"; the rest is "wrong capital".

**Expected output:**

```
[2, 0, 2]
```
