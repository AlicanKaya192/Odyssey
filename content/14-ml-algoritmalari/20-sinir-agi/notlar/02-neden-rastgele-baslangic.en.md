In the lesson the weights started at random (`rng.normal`). What if they all
started at zero, or all at the same number? Let us train the lesson's
10-neuron network on the moons data with three starts and count, after
training, how many **distinct** columns of `W₁` (distinct hidden neurons)
remain:

```python
for name, value in (("zeros", 0.0), ("same", 0.5), ("random", None)):
    P = init(2, 10)
    if value is not None:
        P["W1"][:] = value
        P["W2"][:] = value
    train(P, Xtr, ytr.astype(float), 0.5, 3000)
    distinct = np.unique(P["W1"].round(6), axis=1).shape[1]
    acc = ((forward(P, Xte)[1] > 0.5) == yte).mean()
    print(name, distinct, round(acc, 3))
```

```text
zeros 1 0.5
same 1 0.93
random 10 0.97
```

**All zeros:** the network learns nothing (accuracy 0.5). The hidden layer's
output is `tanh(0) = 0` and the output weights are zero too, so the
derivatives of both layers come out zero; only the output's constant term
changes and the network gives every point the same answer.

**All the same (0.5):** the 10 neurons stay **identical** throughout training
(1 distinct column). They all see the same input and get the same
derivative, so nothing tells them apart; the 10-neuron network is really a
one-neuron network. Accuracy 0.93: the level of logistic regression.

**Random:** all 10 neurons are distinct, accuracy 0.97.

This is called the **symmetry problem**. A random start breaks the symmetry:
each neuron starts from a different place and learns something different.
The **scale** of the weights matters too; deep networks use starts tuned to
the layer width (such as Xavier or He).
