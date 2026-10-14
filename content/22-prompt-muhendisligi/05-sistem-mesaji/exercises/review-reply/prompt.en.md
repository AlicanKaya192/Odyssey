`review(reply, max_sentences)` should check the three rules of the lesson
and return the problems it finds in this order: `"too long"` if the
number of sentences (`re.split(r"[.!?]+", reply)`, empty pieces not
counted) exceeds `max_sentences`; `"promise"` if the given `PROMISE`
pattern is found; `"talks about itself"` if the words `as an ai` appear,
ignoring case (`r"\bas an ai\b"`).

**Expected output:**

```
['promise']
['too long']
['talks about itself']
```
