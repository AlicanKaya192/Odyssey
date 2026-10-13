Why did we start the weights randomly? Let us start them all at zero and
train for ten epochs with the lesson's `forward`, `backward` and training
loop:

```python
def train(P, epochs=10, seed=1):
    rng = np.random.default_rng(seed)
    for _ in range(epochs):
        order = rng.permutation(len(y_train))
        for start in range(0, len(order), 32):
            batch = order[start:start + 32]
            grads = backward(P, A_train[batch], y_train[batch])
            for name in P:
                P[name] -= 0.5 * grads[name]
    return round(float((predict(P, A_test) == y_test).mean()), 3)


zeros = {name: np.zeros_like(value) for name, value in params.items()}
print(train(zeros))
print(np.bincount(predict(zeros, A_test)), round(float((y_test == 2).mean()), 3))
```

```text
0.66
[  0   0 500] 0.66
```

- The network started at zero calls every review "positive"; its accuracy
  equals the baseline. It learned nothing.
- The reason: if `W1` and `W2` are zero, the hidden layer is always 0 and the
  derivative coming back is 0 too. Only the output bias (`b2`) learns, and it
  picks the most frequent class.
- Even if not zero, an **equal** start does not work: neurons starting with
  the same value get the same derivative and stay the same forever
  (symmetry). A random start breaks the symmetry. In the lesson the scale
  `sqrt(2 / inputs)` for `W1` is the start recommended for ReLU (He
  initialisation).
