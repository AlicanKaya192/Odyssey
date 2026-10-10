import numpy as np

rng = np.random.default_rng(1)
x = rng.uniform(-3, 3, 200)
y = 2 * np.sin(x) + rng.normal(0, 0.3, 200)
X = x.reshape(-1, 1)
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def poly_score(degree):
    model = make_pipeline(StandardScaler(), Ridge(alpha=1e-3))
    cv = KFold(5, shuffle=True, random_state=0)
    return round(float(cross_val_score(model, X, y, cv=cv).mean()), 3)

print(poly_score(1))
print(poly_score(3))
