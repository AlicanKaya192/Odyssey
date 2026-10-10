from sklearn.datasets import load_digits

X, y = load_digits(return_X_y=True)
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def pca_accuracy(n):
    model = make_pipeline(StandardScaler(), PCA(n_components=n), LogisticRegression(max_iter=2000))
    return round(float(cross_val_score(model, X, y, cv=5).mean()), 3)

print(pca_accuracy(10))
print(pca_accuracy(30))
