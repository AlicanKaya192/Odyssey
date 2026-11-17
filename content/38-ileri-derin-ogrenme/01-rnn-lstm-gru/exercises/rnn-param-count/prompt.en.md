`rnn_param_count(kind, input_size, hidden_size)` should build an `nn.RNN`,
`nn.GRU` or `nn.LSTM` depending on whether `kind` is `"rnn"`, `"gru"` or
`"lstm"`, and return the total number of its parameters.

**Expected output:**

```
27
81
640
```
