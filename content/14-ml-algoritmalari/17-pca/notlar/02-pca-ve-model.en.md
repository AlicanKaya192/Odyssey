PCA is often used not alone but before a model: training with 20 components
instead of 64 features is faster. But how much accuracy is lost? On the
lesson's digit data, let us measure logistic regression with different `k`s
using 5-fold cross-validation. Scaling and PCA are inside a `Pipeline`: in
each fold they fit only the training part, and the test part does not leak.

```python
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

digits = load_digits()
for k in (5, 10, 20, 40, 64):
    model = make_pipeline(StandardScaler(), PCA(k),
                          LogisticRegression(max_iter=2000))
    score = cross_val_score(model, digits.data, digits.target, cv=5).mean()
    print(k, round(score, 3))
```

```text
5 0.771
10 0.84
20 0.899
40 0.914
64 0.92
```

With all 64 components (just a rotation) the accuracy is 0.92. With 20
components 0.899, with 40 0.914: most of the accuracy is kept with less than a
third of the features. At 5 components it drops to 0.771; too much
information was thrown away here.

This table shows that PCA is a **trade-off**: a little accuracy in exchange
for fewer features, a faster model and less risk of overfitting. Choosing `k`
with cross-validation, like any other setting, is the safest. A warning: PCA
does not see the target; the directions carrying the most variance are not
always the ones that separate the classes best.
