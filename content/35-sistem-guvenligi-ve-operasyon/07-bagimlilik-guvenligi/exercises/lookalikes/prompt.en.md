`lookalikes(names, popular)` should return, in the order of `names`, a
`"<name> -> <popular>"` line for every name that is **not** in `popular`
but is very similar to a popular name. Similarity:
`difflib.get_close_matches(name, popular, n=1, cutoff=0.8)`. A popular name
itself and a name resembling nothing are not listed.

**Expected output:**

```
numpi -> numpy
flaskk -> flask
```
