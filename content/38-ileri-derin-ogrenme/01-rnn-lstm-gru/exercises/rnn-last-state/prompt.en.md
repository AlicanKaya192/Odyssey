`rnn_last_state(xs, w_ih, w_hh)` should run an RNN without biases by hand: the
hidden state starts as zeros (as many as `w_ih` has rows), and at every step
`h = tanh(x @ w_ih.T + h @ w_hh.T)`. Return the last hidden state as a list
with 3 places.

**Expected output:**

```
[0.0, 0.462]
[0.432, 0.462]
```
