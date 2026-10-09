# Regularisation

In section 3 we saw two problems: with collinear features the weights grew
meaninglessly, and a high-degree polynomial fitted the training points too
closely. The common cure for both is **regularisation**: adding a penalty for
the size of the weights to the loss. The model no longer says "make the error
small" but "make the error small while keeping the weights small too".

## Ridge: the squares penalty

**Ridge** adds `α Σ wᵢ²` to the loss. The normal equation changes by a single
term: `(Xᵀ X + α I) w = Xᵀ y`. The intercept is not penalised; for that, `X` and
`y` are first freed of their means (centred), and the intercept is found
afterwards.

```python
import numpy as np

rng = np.random.default_rng(7)
n = 60
X = rng.normal(0, 1, size=(n, 8))
# only the first three matter
true_w = np.array([3.0, -2.0, 1.5, 0, 0, 0, 0, 0])
y = 1.0 + X @ true_w + rng.normal(0, 1.0, n)


def ridge(X, y, alpha):
    xm, ym = X.mean(axis=0), y.mean()
    # centre: no intercept penalty
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return ym - xm @ w, w


from sklearn.linear_model import Ridge

b, w = ridge(X, y, 10.0)
ref = Ridge(alpha=10.0).fit(X, y)
print(np.allclose(w, ref.coef_), np.isclose(b, ref.intercept_))
for alpha in (0.0, 10.0, 100.0, 1000.0):
    b, w = ridge(X, y, alpha)
    print(alpha, w[:3].round(2), round(float(np.abs(w).sum()), 2))
```

```text
True True
0.0 [ 2.88 -2.09  1.56] 7.42
10.0 [ 2.37 -1.69  1.36] 6.27
100.0 [ 0.94 -0.64  0.64] 2.79
1000.0 [ 0.14 -0.09  0.1 ] 0.43
```

The same as scikit-learn's `Ridge`. As `α` grows, the weights **shrink**
towards zero: `α = 0` is ordinary least squares, at `α = 1000` the weights are
almost zero. The right `α` is in between; it is chosen with cross-validation.

## Lasso: the absolute value penalty

**Lasso** adds `α Σ |wᵢ|` to the loss. It has no closed formula; **coordinate
descent** moves the weights one at a time to their best value while the others
are fixed, round after round. A weight's best value is found with **soft
thresholding**: small contributions are pulled to exactly zero.

```python
def soft(z, t):
    return np.sign(z) * max(abs(z) - t, 0.0)          # exactly 0 if |z| ≤ t


def lasso(X, y, alpha, rounds=200):
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    n, d = Xc.shape
    w = np.zeros(d)
    for _ in range(rounds):
        for j in range(d):
            resid = yc - Xc @ w + Xc[:, j] * w[j]     # residual without j
            rho = Xc[:, j] @ resid / n
            w[j] = soft(rho, alpha) / (Xc[:, j] @ Xc[:, j] / n)
    return ym - xm @ w, w


from sklearn.linear_model import Lasso

b, w = lasso(X, y, 0.2)
ref = Lasso(alpha=0.2).fit(X, y)
print(w.round(3))
print(ref.coef_.round(3), np.allclose(w, ref.coef_, atol=1e-4))
b0, w0 = ridge(X, y, 0.0)
print(w0[3:].round(3))
```

```text
[ 2.654 -1.846  1.393  0.037  0.061  0.     0.     0.   ]
[ 2.654 -1.846  1.393  0.037  0.061  0.     0.     0.   ] True
[0.257 0.187 0.15  0.061 0.246]
```

Lasso found the same weights as scikit-learn. It set three of the five useless
features to **exactly zero** and brought the other two down to 0.04 and 0.06;
in the unregularised model the same five were between 0.06 and 0.26. So Lasso
also does **feature selection**. Ridge shrinks the weights but does not make
them zero.

<figure class="fig">
<svg viewBox="0 0 460 275" width="460" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="20" y1="150" x2="200" y2="150"/><line class="grid" x1="110" y1="40" x2="110" y2="230"/><polygon class="box" points="110,95 165,150 110,205 55,150" fill-opacity=".3"/><circle class="curve2" cx="130" cy="60" r="40.3" fill="none"/><circle class="curve2" cx="130" cy="60" r="26.2" fill="none"/><circle class="curve2" cx="130" cy="60" r="12.1" fill="none"/><circle class="dot" cx="110.0" cy="95.0" r="5"/><text class="ink" x="110" y="262" font-size="12" text-anchor="middle">Lasso (L1)</text><line class="grid" x1="260" y1="150" x2="440" y2="150"/><line class="grid" x1="350" y1="40" x2="350" y2="230"/><circle class="box" cx="350" cy="150" r="55" fill-opacity=".3"/><circle class="curve2" cx="370" cy="60" r="37.2" fill="none"/><circle class="curve2" cx="370" cy="60" r="24.2" fill="none"/><circle class="curve2" cx="370" cy="60" r="11.2" fill="none"/><circle class="dot" cx="361.9" cy="96.3" r="5"/><text class="ink" x="350" y="262" font-size="12" text-anchor="middle">Ridge (L2)</text></svg>
<figcaption>The penalty region (grey) and the error contours (orange). The best point (purple) is where a contour first touches the region: on Lasso's cornered region often on an axis, so one weight is exactly zero; not on Ridge's round region.</figcaption>
</figure>

## A cure for collinearity

Let us rebuild section 3's problem in a small example: `x₂` is almost `x₁`.

```python
x1 = rng.normal(0, 1, n)
x2 = x1 + rng.normal(0, 0.01, n)
yc = 2 * x1 + rng.normal(0, 0.5, n)
Xc2 = np.column_stack([x1, x2])
for alpha in (0.0, 1.0):
    print(alpha, ridge(Xc2, yc, alpha)[1].round(2))
```

```text
0.0 [ 15.7 -13.7]
1.0 [1.01 0.93]
```

Without regularisation the weights are 15.7 and −13.7; with a small `α = 1`,
1.01 and 0.93: the effect was shared between the two copies, and their sum is
still about 2. The penalty closes the "cancel each other out with large
weights" route.

## A cure for overfitting

This time we build the degree-9 polynomial with 20 points and with Ridge. Since
the polynomial features have very different scales, they are standardised
first.

```python
xs = rng.uniform(-3, 3, 20)
ys = np.sin(xs) + rng.normal(0, 0.2, 20)
xt = rng.uniform(-3, 3, 300)
yt = np.sin(xt) + rng.normal(0, 0.2, 300)
P = lambda x: np.column_stack([x ** d for d in range(1, 10)])
mu, sd = P(xs).mean(axis=0), P(xs).std(axis=0)
# with the training scale
S = lambda x: (P(x) - mu) / sd
for alpha in (0.0, 0.01, 0.1, 1.0, 10.0):
    b, w = ridge(S(xs), ys, alpha)
    test = ((b + S(xt) @ w - yt) ** 2).mean()
    print(alpha, round(test, 4))
```

```text
0.0 0.0934
0.01 0.0679
0.1 0.0778
1.0 0.1207
10.0 0.2164
```

The test error is 0.093 at `α = 0`, lowest at `α = 0.01` with 0.068, then rises
again: too much penalty makes the model too simple as well (**underfitting**).
Regularisation is the way to tune model complexity with a single knob.

## Summary

- Ridge: loss + `α Σ w²`; solution `(Xᵀ X + α I) w = Xᵀ y`, no penalty on the
  intercept.
- Lasso: loss + `α Σ |w|`; coordinate descent and soft thresholding; it makes
  some weights exactly zero (feature selection).
- It makes weights stable under collinearity and reduces overfitting.
- If `α` is too small, overfitting; too large, underfitting; it is chosen with
  cross-validation.
- The penalty is scale-sensitive: standardise first.
