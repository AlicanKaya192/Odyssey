`run_rnn(xs, Wx, Wh, b)` should start the hidden state with zeros (of `b`'s
length), take the step `tanh(x @ Wx + h @ Wh + b)` with each input in `xs`,
and return the last hidden state as a list with 3 places. The same inputs in
reverse order should give a different result.

**Expected output:**

```
[-0.253, 0.553]
[0.551, 0.363]
```
