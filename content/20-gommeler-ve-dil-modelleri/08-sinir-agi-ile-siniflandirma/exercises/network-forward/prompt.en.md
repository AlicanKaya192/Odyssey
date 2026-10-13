`forward(A, E, W1, W2)` should run the lesson's forward pass (no biases):
`x = A @ E`, `h = ReLU(x @ W1)`, `p = softmax(h @ W2)`. Return the
probabilities as a list of lists with 3 places.

**Expected output:**

```
[[0.679, 0.321]]
[[0.731, 0.269], [0.378, 0.622]]
```
