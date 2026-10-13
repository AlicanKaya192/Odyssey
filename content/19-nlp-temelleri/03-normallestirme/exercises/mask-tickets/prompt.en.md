`mask(text)` should apply every `(pattern, placeholder)` pair in `RULES` **in
order** with `re.sub`. The second line of the output is the vocabulary of
1000 tickets after the placeholders.

**Expected output:**

```
Paid <money> on <order>, mail <email>
329
```
