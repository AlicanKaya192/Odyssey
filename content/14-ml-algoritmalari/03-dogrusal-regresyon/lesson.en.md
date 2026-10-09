# Linear Regression

Linear regression predicts a number (a price, a duration, a temperature) as a
weighted sum of the features: `ŷ = w₀ + w₁x₁ + w₂x₂ + …`. The weights are chosen
to make the sum of the squared prediction errors as small as possible (**least
squares**). In this section we find the weights with a single formula, measure
the performance and see where the formula struggles.

## The normal equation

If we add a column of `1`s at the front of the feature matrix (for the
intercept, `w₀`), the whole model becomes `ŷ = A w`. The `w` that minimises the
squared errors is the solution of the **normal equation**: `(Aᵀ A) w = Aᵀ y`.

```python
import numpy as np

rng = np.random.default_rng(3)
X = rng.uniform(0, 10, size=(100, 2))
# the true weights: 3, 2, -1.5
y = 3 + 2 * X[:, 0] - 1.5 * X[:, 1] + rng.normal(0, 1, 100)


def fit_linear(X, y):
    A = np.column_stack([np.ones(len(X)), X])     # the 1 column: intercept
    return np.linalg.solve(A.T @ A, A.T @ y)


def predict_linear(w, X):
    return w[0] + X @ w[1:]


w = fit_linear(X, y)
print(w.round(3))
from sklearn.linear_model import LinearRegression

ref = LinearRegression().fit(X, y)
same = np.allclose(w, [ref.intercept_, *ref.coef_])
print(round(ref.intercept_, 3), ref.coef_.round(3), same)
```

```text
[ 3.296  1.993 -1.534]
3.296 [ 1.993 -1.534] True
```

We generated the data with `3 + 2x₁ − 1.5x₂` plus noise; the model found 3.296,
1.993 and −1.534. The same as scikit-learn's `LinearRegression`. Using `solve`
instead of computing the inverse matrix explicitly (`np.linalg.inv`) is both
faster and numerically sounder.

## Measuring performance: MSE and R²

The **mean squared error (MSE)** is the mean of the squared errors; its unit is
the square of the target's. **R²** is how much of the error the model explains
compared with the "always say the mean" baseline: 1 is perfect, 0 is as good as
the baseline.

```python
def mse(y, p):
    return ((y - p) ** 2).mean()


def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


from sklearn.metrics import mean_squared_error, r2_score

p = predict_linear(w, X)
print(round(mse(y, p), 4), round(mean_squared_error(y, p), 4))
print(round(r2(y, p), 4), round(r2_score(y, p), 4))
print(round(r2(y, np.full(len(y), y.mean())), 4))
```

```text
0.8896 0.8896
0.9818 0.9818
0.0
```

MSE is 0.89: since the noise variance is 1, getting much lower is not possible.
R² is 0.98; the model always saying the mean scores exactly 0. On test data R²
can even be negative: if the model is worse than the mean.

## Collinearity: two almost identical features

Let us add a third feature that is almost the same as `x₁`. The matrix `Aᵀ A`
becomes nearly singular: its **condition number** grows huge and the weights
become unstable.

```python
x3 = X[:, 0] + rng.normal(0, 0.001, 100)          # an almost-copy of x1
Xc = np.column_stack([X, x3])
A = np.column_stack([np.ones(100), Xc])
print(f"{np.linalg.cond(A.T @ A):.1e}")
wc = np.linalg.lstsq(A, y, rcond=None)[0]
print(wc.round(1))
print(round(mse(y, A @ wc), 4))
```

```text
1.8e+08
[  3.3 -21.8  -1.5  23.8]
0.8891
```

The condition number is around 10⁸. The weights are −21.8 for `x₁` and +23.8
for `x₃`: their sum is still about 2, but one by one they are meaningless. The
error is almost the same (0.889); the model keeps predicting, but reading "when
x₁ goes up by one, y drops by 21.8" is wrong. With collinearity the weights are
not interpreted; regularisation in section 7 softens this problem.

## Polynomials: a linear model, a curved prediction

"Linear" refers to the weights: if we make the features `x, x², x³, …`, the same
method fits a curve. But as the degree grows, the model fits the training
points too closely.

```python
xs = rng.uniform(-3, 3, 15)
ys = np.sin(xs) + rng.normal(0, 0.2, 15)          # 15 training points
xt = rng.uniform(-3, 3, 200)
yt = np.sin(xt) + rng.normal(0, 0.2, 200)         # 200 test points


def poly(x, degree):
    return np.column_stack([x ** d for d in range(1, degree + 1)])


for degree in (1, 3, 9):
    wp = fit_linear(poly(xs, degree), ys)
    train_err = mse(ys, predict_linear(wp, poly(xs, degree)))
    test_err = mse(yt, predict_linear(wp, poly(xt, degree)))
    print(degree, round(train_err, 4), round(test_err, 4))
```

```text
1 0.1491 0.3203
3 0.0324 0.0748
9 0.0082 397.6073
```

As the degree grows, the training error keeps falling (0.149 → 0.032 → 0.008).
The test error, however, is best at degree 3 (0.075) and 397 at degree 9: the
model swings wildly between the 15 points and explodes at the ends. This is
**overfitting**: a low training error with a large test error.

<figure class="fig">
<svg viewBox="0 0 520 260" width="520" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="20" y1="130" x2="500" y2="130"/><polyline class="curve" points="20.0,160.2 22.0,162.9 24.0,165.6 26.0,168.2 28.0,170.7 30.0,173.1 32.0,175.5 34.0,177.8 36.0,180.0 38.0,182.2 40.0,184.2 42.0,186.2 44.0,188.2 46.0,190.0 48.0,191.8 50.0,193.5 52.0,195.2 54.0,196.8 56.0,198.3 58.0,199.7 60.0,201.1 62.0,202.4 64.0,203.7 66.0,204.9 68.0,206.0 70.0,207.1 72.0,208.1 74.0,209.0 76.0,209.9 78.0,210.7 80.0,211.5 82.0,212.2 84.0,212.8 86.0,213.4 88.0,213.9 90.0,214.4 92.0,214.8 94.0,215.2 96.0,215.5 98.0,215.7 100.0,215.9 102.0,216.1 104.0,216.2 106.0,216.3 108.0,216.3 110.0,216.2 112.0,216.1 114.0,216.0 116.0,215.8 118.0,215.5 120.0,215.3 122.0,214.9 124.0,214.6 126.0,214.1 128.0,213.7 130.0,213.2 132.0,212.6 134.0,212.0 136.0,211.4 138.0,210.8 140.0,210.0 142.0,209.3 144.0,208.5 146.0,207.7 148.0,206.9 150.0,206.0 152.0,205.0 154.0,204.1 156.0,203.1 158.0,202.1 160.0,201.0 162.0,199.9 164.0,198.8 166.0,197.6 168.0,196.5 170.0,195.3 172.0,194.0 174.0,192.8 176.0,191.5 178.0,190.1 180.0,188.8 182.0,187.4 184.0,186.0 186.0,184.6 188.0,183.2 190.0,181.7 192.0,180.2 194.0,178.7 196.0,177.2 198.0,175.7 200.0,174.1 202.0,172.5 204.0,170.9 206.0,169.3 208.0,167.7 210.0,166.0 212.0,164.4 214.0,162.7 216.0,161.0 218.0,159.3 220.0,157.6 222.0,155.9 224.0,154.1 226.0,152.4 228.0,150.6 230.0,148.9 232.0,147.1 234.0,145.3 236.0,143.5 238.0,141.7 240.0,139.9 242.0,138.1 244.0,136.3 246.0,134.5 248.0,132.7 250.0,130.9 252.0,129.1 254.0,127.2 256.0,125.4 258.0,123.6 260.0,121.8 262.0,120.0 264.0,118.2 266.0,116.4 268.0,114.6 270.0,112.8 272.0,111.0 274.0,109.2 276.0,107.4 278.0,105.6 280.0,103.9 282.0,102.1 284.0,100.4 286.0,98.6 288.0,96.9 290.0,95.2 292.0,93.5 294.0,91.8 296.0,90.1 298.0,88.4 300.0,86.8 302.0,85.2 304.0,83.5 306.0,81.9 308.0,80.4 310.0,78.8 312.0,77.3 314.0,75.7 316.0,74.2 318.0,72.7 320.0,71.3 322.0,69.8 324.0,68.4 326.0,67.0 328.0,65.7 330.0,64.3 332.0,63.0 334.0,61.7 336.0,60.4 338.0,59.2 340.0,58.0 342.0,56.8 344.0,55.7 346.0,54.5 348.0,53.4 350.0,52.4 352.0,51.4 354.0,50.4 356.0,49.4 358.0,48.5 360.0,47.6 362.0,46.7 364.0,45.9 366.0,45.1 368.0,44.4 370.0,43.7 372.0,43.0 374.0,42.4 376.0,41.8 378.0,41.2 380.0,40.7 382.0,40.3 384.0,39.9 386.0,39.5 388.0,39.2 390.0,38.9 392.0,38.6 394.0,38.4 396.0,38.3 398.0,38.2 400.0,38.1 402.0,38.1 404.0,38.2 406.0,38.3 408.0,38.4 410.0,38.6 412.0,38.9 414.0,39.2 416.0,39.6 418.0,40.0 420.0,40.5 422.0,41.0 424.0,41.6 426.0,42.2 428.0,42.9 430.0,43.7 432.0,44.5 434.0,45.4 436.0,46.3 438.0,47.3 440.0,48.4 442.0,49.5 444.0,50.7 446.0,51.9 448.0,53.2 450.0,54.6 452.0,56.0 454.0,57.6 456.0,59.1 458.0,60.8 460.0,62.5 462.0,64.3 464.0,66.1 466.0,68.1 468.0,70.1 470.0,72.1 472.0,74.3 474.0,76.5 476.0,78.8 478.0,81.1 480.0,83.6 482.0,86.1 484.0,88.7 486.0,91.4 488.0,94.1 490.0,96.9 492.0,99.8 494.0,102.8 496.0,105.9 498.0,109.0 500.0,112.3" fill="none"/><polyline class="curve2" points="94.0,237.7 96.0,224.0 98.0,213.0 100.0,204.3 102.0,197.6 104.0,192.6 106.0,189.1 108.0,186.9 110.0,185.8 112.0,185.7 114.0,186.3 116.0,187.6 118.0,189.3 120.0,191.4 122.0,193.9 124.0,196.5 126.0,199.2 128.0,202.0 130.0,204.7 132.0,207.4 134.0,210.0 136.0,212.4 138.0,214.6 140.0,216.6 142.0,218.5 144.0,220.0 146.0,221.3 148.0,222.4 150.0,223.2 152.0,223.7 154.0,224.0 156.0,224.0 158.0,223.8 160.0,223.3 162.0,222.6 164.0,221.7 166.0,220.6 168.0,219.3 170.0,217.8 172.0,216.2 174.0,214.3 176.0,212.4 178.0,210.3 180.0,208.1 182.0,205.8 184.0,203.4 186.0,201.0 188.0,198.4 190.0,195.9 192.0,193.2 194.0,190.6 196.0,187.9 198.0,185.2 200.0,182.5 202.0,179.8 204.0,177.1 206.0,174.5 208.0,171.8 210.0,169.2 212.0,166.6 214.0,164.0 216.0,161.5 218.0,159.0 220.0,156.6 222.0,154.2 224.0,151.8 226.0,149.5 228.0,147.2 230.0,144.9 232.0,142.7 234.0,140.6 236.0,138.5 238.0,136.4 240.0,134.3 242.0,132.3 244.0,130.3 246.0,128.4 248.0,126.5 250.0,124.6 252.0,122.7 254.0,120.8 256.0,119.0 258.0,117.2 260.0,115.4 262.0,113.6 264.0,111.9 266.0,110.1 268.0,108.3 270.0,106.6 272.0,104.9 274.0,103.1 276.0,101.4 278.0,99.7 280.0,97.9 282.0,96.2 284.0,94.5 286.0,92.8 288.0,91.1 290.0,89.4 292.0,87.7 294.0,86.0 296.0,84.3 298.0,82.6 300.0,81.0 302.0,79.3 304.0,77.7 306.0,76.0 308.0,74.4 310.0,72.8 312.0,71.3 314.0,69.7 316.0,68.2 318.0,66.6 320.0,65.2 322.0,63.7 324.0,62.3 326.0,60.9 328.0,59.5 330.0,58.2 332.0,56.9 334.0,55.7 336.0,54.5 338.0,53.3 340.0,52.2 342.0,51.1 344.0,50.1 346.0,49.1 348.0,48.2 350.0,47.3 352.0,46.5 354.0,45.7 356.0,45.0 358.0,44.3 360.0,43.7 362.0,43.2 364.0,42.6 366.0,42.2 368.0,41.8 370.0,41.4 372.0,41.1 374.0,40.8 376.0,40.6 378.0,40.5 380.0,40.4 382.0,40.3 384.0,40.3 386.0,40.4 388.0,40.5 390.0,40.6 392.0,40.8 394.0,41.1 396.0,41.4 398.0,41.7 400.0,42.1 402.0,42.5 404.0,43.0 406.0,43.6 408.0,44.2 410.0,44.9 412.0,45.6 414.0,46.3 416.0,47.2 418.0,48.0 420.0,49.0 422.0,50.0 424.0,51.1 426.0,52.2 428.0,53.4 430.0,54.7 432.0,56.0 434.0,57.4 436.0,58.9 438.0,60.4 440.0,62.0 442.0,63.7 444.0,65.4 446.0,67.2 448.0,69.0 450.0,70.9 452.0,72.8 454.0,74.7 456.0,76.6 458.0,78.5 460.0,80.3 462.0,82.1 464.0,83.9 466.0,85.5 468.0,87.0 470.0,88.3 472.0,89.3 474.0,90.1 476.0,90.6 478.0,90.6 480.0,90.2 482.0,89.3 484.0,87.7 486.0,85.4 488.0,82.3 490.0,78.3 492.0,73.1 494.0,66.8 496.0,59.1 498.0,49.8 500.0,38.9" fill="none"/><polyline class="curve3" points="20.0,141.3 24.0,145.2 28.0,149.1 32.0,153.0 36.0,156.8 40.0,160.5 44.0,164.2 48.0,167.8 52.0,171.2 56.0,174.6 60.0,177.9 64.0,181.0 68.0,184.0 72.0,186.9 76.0,189.7 80.0,192.2 84.0,194.7 88.0,197.0 92.0,199.1 96.0,201.0 100.0,202.7 104.0,204.3 108.0,205.7 112.0,206.9 116.0,207.9 120.0,208.7 124.0,209.3 128.0,209.7 132.0,210.0 136.0,210.0 140.0,209.8 144.0,209.4 148.0,208.8 152.0,208.1 156.0,207.1 160.0,205.9 164.0,204.6 168.0,203.0 172.0,201.3 176.0,199.4 180.0,197.3 184.0,195.1 188.0,192.7 192.0,190.1 196.0,187.4 200.0,184.5 204.0,181.5 208.0,178.4 212.0,175.2 216.0,171.8 220.0,168.4 224.0,164.8 228.0,161.2 232.0,157.4 236.0,153.6 240.0,149.8 244.0,145.9 248.0,142.0 252.0,138.0 256.0,134.0 260.0,130.0 264.0,126.0 268.0,122.0 272.0,118.0 276.0,114.1 280.0,110.2 284.0,106.4 288.0,102.6 292.0,98.8 296.0,95.2 300.0,91.6 304.0,88.2 308.0,84.8 312.0,81.6 316.0,78.5 320.0,75.5 324.0,72.6 328.0,69.9 332.0,67.3 336.0,64.9 340.0,62.7 344.0,60.6 348.0,58.7 352.0,57.0 356.0,55.4 360.0,54.1 364.0,52.9 368.0,51.9 372.0,51.2 376.0,50.6 380.0,50.2 384.0,50.0 388.0,50.0 392.0,50.3 396.0,50.7 400.0,51.3 404.0,52.1 408.0,53.1 412.0,54.3 416.0,55.7 420.0,57.3 424.0,59.0 428.0,60.9 432.0,63.0 436.0,65.3 440.0,67.8 444.0,70.3 448.0,73.1 452.0,76.0 456.0,79.0 460.0,82.1 464.0,85.4 468.0,88.8 472.0,92.2 476.0,95.8 480.0,99.5 484.0,103.2 488.0,107.0 492.0,110.9 496.0,114.8 500.0,118.7" fill="none"/><circle class="dot" cx="119.8" cy="206.3" r="4"/><circle class="dot" cx="362.8" cy="44.6" r="4"/><circle class="dot" cx="211.0" cy="163.6" r="4"/><circle class="dot" cx="183.8" cy="207.7" r="4"/><circle class="dot" cx="487.7" cy="82.8" r="4"/><circle class="dot" cx="449.0" cy="70.1" r="4"/><circle class="dot" cx="125.1" cy="177.1" r="4"/><circle class="dot" cx="94.6" cy="233.0" r="4"/><circle class="dot" cx="256.3" cy="122.4" r="4"/><circle class="dot" cx="295.6" cy="79.9" r="4"/><circle class="dot" cx="186.4" cy="199.1" r="4"/><circle class="dot" cx="303.9" cy="81.0" r="4"/><circle class="dot" cx="345.5" cy="47.9" r="4"/><circle class="dot" cx="411.0" cy="44.7" r="4"/><circle class="dot" cx="136.2" cy="218.6" r="4"/></svg>
<figcaption>15 training points (purple), the true curve sin x (grey). Degree 3 (purple) is close to the curve; degree 9 (orange) swings to get near all the points and shoots off the chart at the ends.</figcaption>
</figure>

## Summary

- The model is `ŷ = A w`; the least squares solution is `(Aᵀ A) w = Aᵀ y`, with
  `np.linalg.solve` or `lstsq`.
- MSE is the mean of the squared errors; R² is the share explained compared
  with the baseline.
- With collinear features the condition number explodes and the weights cannot
  be interpreted.
- With polynomial features a linear model fits curves; as the degree grows,
  overfitting makes the test error explode.
