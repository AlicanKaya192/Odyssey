The read-only `tiny_chat.py` holds the lesson's toy model.
`gate(country, n, threshold)` should ask the question `n` times with
`ask(country, temperature=1.0, seed=s)` for `s = 0, 1, …, n-1`, find the most
common answer and its share (on a tie the one first in alphabetical order).
If the share is not below `threshold` return the answer, otherwise
`"I am not sure."`.

**Expected output:**

```
japan the capital of japan is tokyo .
chile I am not sure.
```
