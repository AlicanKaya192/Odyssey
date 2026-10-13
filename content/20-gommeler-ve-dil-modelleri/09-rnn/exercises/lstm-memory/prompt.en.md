`lstm_memory(forgets, writes, news)` should start the cell state at `0` and
update it at every step with `c = f · c + i · g` (`f` the forget gate, `i`
the input gate, `g` the new information). Return the cell value after every
step in a list with 3 places.

**Expected output:**

```
[0.8, 0.8, 0.8]
[1.0, 0.5, -0.3]
```
