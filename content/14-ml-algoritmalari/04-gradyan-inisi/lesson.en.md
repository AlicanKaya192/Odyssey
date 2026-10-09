# Gradient Descent

Linear regression had a closed formula. Most models do not: we cannot find the
weights of logistic regression or a neural network with a single equation. We
find them with **gradient descent**: taking small steps against the direction
in which the error grows fastest (the gradient). In this section we build the
method on linear regression and compare its result with the closed formula; so
we can be sure it works.

## Gradient and step

The loss is `L(w) = mean((A w − y)²)`. Its gradient is
`∇L = (2/n) Aᵀ (A w − y)`: for each weight, "how much does the loss grow if I
raise this weight a little". One step: `w ← w − η ∇L`; `η` is the **learning
rate**.

<figure class="fig">
<svg viewBox="0 0 480 220" width="480" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="50" y1="190" x2="460" y2="190"/><line class="grid" x1="50" y1="15" x2="50" y2="190"/><text class="dim" x="44" y="175.9" font-size="11" text-anchor="end">0.1</text><text class="dim" x="44" y="115.6" font-size="11" text-anchor="end">1</text><text class="dim" x="44" y="55.3" font-size="11" text-anchor="end">10</text><polyline class="curve3" points="50.0,30.8 56.9,32.4 63.9,34.1 70.8,35.7 77.8,37.3 84.7,38.9 91.7,40.4 98.6,42.0 105.6,43.6 112.5,45.1 119.5,46.7 126.4,48.2 133.4,49.8 140.3,51.3 147.3,52.8 154.2,54.3 161.2,55.8 168.1,57.2 175.1,58.7 182.0,60.1 189.0,61.6 195.9,63.0 202.9,64.4 209.8,65.7 216.8,67.1 223.7,68.4 230.7,69.8 237.6,71.1 244.6,72.3 251.5,73.6 258.5,74.9 265.4,76.1 272.4,77.3 279.3,78.5 286.3,79.6 293.2,80.7 300.2,81.8 307.1,82.9 314.1,84.0 321.0,85.0 328.0,86.0 334.9,87.0 341.9,88.0 348.8,88.9 355.8,89.8 362.7,90.7 369.7,91.5 376.6,92.3 383.6,93.1 390.5,93.9 397.5,94.7 404.4,95.4 411.4,96.1 418.3,96.8 425.3,97.4 432.2,98.1 439.2,98.7 446.1,99.2 453.1,99.8 460.0,100.3" fill="none"/><text class="ink" x="462" y="94.3" font-size="11" text-anchor="end">η = 0.01</text><polyline class="curve2" points="50.0,30.8 56.9,49.6 63.9,66.7 70.8,81.3 77.8,92.5 84.7,100.1 91.7,104.8 98.6,107.7 105.6,109.5 112.5,110.7 119.5,111.7 126.4,112.5 133.4,113.3 140.3,114.1 147.3,114.8 154.2,115.6 161.2,116.3 168.1,117.0 175.1,117.7 182.0,118.5 189.0,119.2 195.9,119.9 202.9,120.6 209.8,121.3 216.8,122.0 223.7,122.7 230.7,123.4 237.6,124.1 244.6,124.8 251.5,125.5 258.5,126.2 265.4,126.8 272.4,127.5 279.3,128.2 286.3,128.9 293.2,129.5 300.2,130.2 307.1,130.8 314.1,131.5 321.0,132.2 328.0,132.8 334.9,133.4 341.9,134.1 348.8,134.7 355.8,135.3 362.7,136.0 369.7,136.6 376.6,137.2 383.6,137.8 390.5,138.4 397.5,139.0 404.4,139.6 411.4,140.2 418.3,140.8 425.3,141.4 432.2,142.0 439.2,142.6 446.1,143.1 453.1,143.7 460.0,144.2" fill="none"/><text class="ink" x="462" y="138.2" font-size="11" text-anchor="end">η = 0.1</text><polyline class="curve" points="50.0,30.8 56.9,54.3 63.9,75.7 70.8,93.8 77.8,107.7 84.7,117.4 91.7,124.1 98.6,129.1 105.6,133.1 112.5,136.6 119.5,139.9 126.4,143.0 133.4,145.8 140.3,148.5 147.3,151.1 154.2,153.5 161.2,155.7 168.1,157.8 175.1,159.7 182.0,161.5 189.0,163.1 195.9,164.5 202.9,165.8 209.8,167.0 216.8,168.1 223.7,169.0 230.7,169.8 237.6,170.6 244.6,171.2 251.5,171.8 258.5,172.3 265.4,172.7 272.4,173.1 279.3,173.4 286.3,173.7 293.2,174.0 300.2,174.2 307.1,174.4 314.1,174.6 321.0,174.7 328.0,174.8 334.9,175.0 341.9,175.0 348.8,175.1 355.8,175.2 362.7,175.3 369.7,175.3 376.6,175.4 383.6,175.4 390.5,175.4 397.5,175.5 404.4,175.5 411.4,175.5 418.3,175.5 425.3,175.6 432.2,175.6 439.2,175.6 446.1,175.6 453.1,175.6 460.0,175.6" fill="none"/><text class="ink" x="462" y="169.6" font-size="11" text-anchor="end">η = 0.5</text><text class="dim" x="265.0" y="212" font-size="11" text-anchor="middle">step</text></svg>
<figcaption>The loss over the first 60 steps with three learning rates on the same data (log vertical axis). η = 0.5 reaches the bottom in a few steps, η = 0.01 is still on its way.</figcaption>
</figure>

```python
import numpy as np

rng = np.random.default_rng(4)
n = 200
X = np.column_stack([rng.uniform(0, 1, n), rng.uniform(0, 1, n)])
y = 4 + 3 * X[:, 0] - 2 * X[:, 1] + rng.normal(0, 0.3, n)
A = np.column_stack([np.ones(n), X])
best = np.linalg.lstsq(A, y, rcond=None)[0]        # closed formula: the target


def loss(w):
    return ((A @ w - y) ** 2).mean()


def gradient(w):
    return 2 / n * A.T @ (A @ w - y)


w = np.zeros(3)
for step in range(1, 2001):
    w -= 0.1 * gradient(w)
    if step in (1, 10, 100, 1000, 2000):
        print(step, round(loss(w), 4), w.round(3))
print(best.round(3), round(loss(best), 4))
```

```text
1 10.6824 [0.912 0.543 0.454]
10 0.9956 [2.86  1.808 1.039]
100 0.145 [ 3.64   2.809 -1.195]
1000 0.0863 [ 4.015  2.955 -2.006]
2000 0.0863 [ 4.015  2.955 -2.006]
[ 4.015  2.955 -2.006] 0.0863
```

Starting from zero, the weights get closer to the target at every step; by the
thousandth step they have reached `[4.015, 2.955, −2.006]`, found by the closed
formula. The loss falls fast in the first ten steps and then more and more
slowly: as the target nears, the gradient shrinks and so do the steps.

## The learning rate

If the learning rate is small, progress is slow; if large, it jumps over the
target and **diverges**: every step is worse than the one before.

```python
for lr in (0.01, 0.1, 0.5, 1.2):
    w = np.zeros(3)
    for _ in range(100):
        w -= lr * gradient(w)
    current = loss(w)
    print(lr, round(current, 4) if current < 1e6 else "diverged")
```

```text
0.01 1.0179
0.1 0.145
0.5 0.0863
1.2 diverged
```

After a hundred steps: with 0.01 still far from the target (1.018), with 0.5
already there (0.0863), with 1.2 the loss shot up to 10⁹³. A good rate is
somewhere just below divergence; in practice a few values are tried (0.001,
0.01, 0.1, …).

## Why scaling is a must

If the features have very different scales (one 0–1000, the other 0–1), the
loss surface turns into a long, narrow valley. A step suitable for the
large-scale feature is far too small for the small-scale one; a single learning
rate does not fit both.

```python
np.seterr(all="ignore")                            # silence overflow warnings
Xb = np.column_stack([rng.uniform(0, 1000, n), rng.uniform(0, 1, n)])
yb = 4 + 0.003 * Xb[:, 0] - 2 * Xb[:, 1] + rng.normal(0, 0.3, n)


def steps_to_converge(Xf, yf, lr, limit=100_000):
    Af = np.column_stack([np.ones(len(Xf)), Xf])
    target = ((Af @ np.linalg.lstsq(Af, yf, rcond=None)[0] - yf) ** 2).mean()
    w = np.zeros(Af.shape[1])
    for step in range(1, limit + 1):
        w -= lr * 2 / len(yf) * Af.T @ (Af @ w - yf)
        if not np.isfinite(w).all():
            return "diverged"
        current = ((Af @ w - yf) ** 2).mean()
        if current <= target * 1.01:               # within 1% of the best
            return step
    return f">{limit}"


print(steps_to_converge(Xb, yb, 1e-6))
print(steps_to_converge(Xb, yb, 1e-5))
Xs = (Xb - Xb.mean(axis=0)) / Xb.std(axis=0)
print(steps_to_converge(Xs, yb, 0.1))
```

```text
>100000
diverged
23
```

On unscaled data the rate `1e-6` could not reach the target even in a hundred
thousand steps; ten times that (`1e-5`) diverged. There may be a narrow usable
band in between, but finding it is a chore. Once the same data was
standardised, **23 steps** were enough with the rate `0.1`. Features are
standardised before gradient descent.

## Mini-batch and stochastic gradient descent

Using all the data at every step is expensive on large data. **Mini-batch**
gradient descent estimates the gradient at every step with a small random group
(20 samples here); an **epoch** is one pass through the data from start to
end. With a group size of 1 it is called **stochastic gradient descent (SGD)**.

```python
batch_rng = np.random.default_rng(0)
w = np.zeros(3)
for epoch in range(20):
    order = batch_rng.permutation(n)                # shuffle every epoch
    for start in range(0, n, 20):
        idx = order[start:start + 20]
        Ab, yb2 = A[idx], y[idx]
        w -= 0.1 * 2 / len(idx) * Ab.T @ (Ab @ w - yb2)
print(w.round(3), round(loss(w), 4), round(loss(best), 4))
```

```text
[ 3.893  2.967 -1.813] 0.0898 0.0863
```

After twenty epochs the loss is 0.0898; the best is 0.0863. Because of the
noisy gradients it does not settle exactly at the bottom but wanders nearby. In
return each step looks at only 20 samples: this is the method used on millions
of rows and in neural networks.

## Checking the gradient

Deriving and writing a gradient by hand, mistakes are easy. Comparing with the
**numerical gradient** `(L(w + ε) − L(w − ε)) / 2ε` catches them:

```python
def numeric_gradient(f, w, eps=1e-6):
    g = np.zeros_like(w)
    for i in range(len(w)):
        step = np.zeros_like(w)
        step[i] = eps
        g[i] = (f(w + step) - f(w - step)) / (2 * eps)
    return g


w0 = np.array([1.0, -1.0, 0.5])
print(gradient(w0).round(5))
print(numeric_gradient(loss, w0).round(5))
print(np.allclose(gradient(w0), numeric_gradient(loss, w0), atol=1e-6))
```

```text
[-7.67332 -4.79231 -3.69183]
[-7.67332 -4.79231 -3.69183]
True
```

The analytic and numerical gradients agree. The numerical way computes the
loss twice for every weight, so it is slow; it is used only for checking.

## Summary

- A step: `w ← w − η ∇L`; for MSE `∇L = (2/n) Aᵀ (A w − y)`.
- A small learning rate is slow, a large one diverges.
- With features of different scales gradient descent gets stuck; standardise
  first (23 steps here instead of more than a hundred thousand).
- Mini-batch/SGD moves with a small group at each step; it wanders near the
  bottom.
- Check the gradient you wrote against the numerical gradient.
