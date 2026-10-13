In the lesson we trained with a single seed. How much does the result depend
on the seed? Let us build and train the same network with five seeds (with
the `train` function of the first note):

```python
scores = []
for seed in range(5):
    rng = np.random.default_rng(seed)
    P = {"E": rng.normal(0, 0.1, (V, 16)),
         "W1": rng.normal(0, np.sqrt(2 / 16), (16, 32)), "b1": np.zeros(32),
         "W2": rng.normal(0, np.sqrt(1 / 32), (32, 3)), "b2": np.zeros(3)}
    scores.append(train(P, epochs=20, seed=seed))
print(scores)
print(round(float(np.mean(scores)), 3), round(float(np.std(scores)), 3))
```

```text
[0.864, 0.88, 0.882, 0.876, 0.868]
0.874 0.007
```

- Five seeds give five different accuracies. The difference comes from the
  starting weights and the order in which the examples are shuffled.
- Comparing two models with a single run can mislead: a difference within
  this range may be the seed's doing. Run with a few seeds and report the
  mean and standard deviation.
- With linear models (logistic regression) this problem is much smaller: the
  loss is convex, and every start leads to the same solution. The loss of a
  neural network has many local solutions.
