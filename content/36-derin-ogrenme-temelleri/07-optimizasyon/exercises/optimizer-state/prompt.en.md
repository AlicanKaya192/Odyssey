`state_names(kind)` should build the optimizer, take a single step with the sum of
`w²` and return the keys in `optimizer.state[w]` as a sorted list.

**Expected output:**

```
sgd []
momentum ['momentum_buffer']
adam ['exp_avg', 'exp_avg_sq', 'step']
```
