How does temperature change a distribution? Let us look at the largest
probability and the **entropy** (the uncertainty of the distribution, in
bits) of the distribution of the word that comes after ", my" (10 options):

```python
probs = list(next_probs(",", "my").values())
for t in [0.1, 0.5, 1.0, 2.0, 10.0]:
    weights = [p ** (1 / t) for p in probs]
    q = [w / sum(weights) for w in weights]
    entropy = -sum(x * math.log2(x) for x in q if x > 0)
    print(t, round(max(q), 3), round(entropy, 2))
print(round(math.log2(len(probs)), 2))
```

```text
0.1 0.985 0.12
0.5 0.595 1.37
1.0 0.446 1.81
2.0 0.305 2.63
10.0 0.136 3.29
3.32
```

- `T = 1` is the model's own distribution. As `T` shrinks, the most likely
  option gathers all the weight; `T → 0` is the same as greedy choice.
- As `T` grows, the distribution flattens and the entropy approaches its
  upper limit (`log2 10` for 10 options): `T → ∞` gives every option an
  equal chance, that is, it throws away what the model knows.
- Temperature does not change what the model knows; it only sets how much
  the choice trusts that knowledge. For tasks wanting a precise answer (code,
  calculation, factual questions) a low temperature is used, for tasks like
  brainstorming a higher one.
