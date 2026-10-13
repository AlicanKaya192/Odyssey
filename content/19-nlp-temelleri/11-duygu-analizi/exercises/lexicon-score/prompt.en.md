`score(text)` should lowercase the text and split it into words with
`re.findall(r"[a-z']+", ...)`; count +1 for every word in `GOOD` and −1 for
every word in `BAD`, and return the total.

**Expected output:**

```
1
-2
0
0
```
