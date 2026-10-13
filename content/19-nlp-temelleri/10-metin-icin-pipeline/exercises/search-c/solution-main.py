import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
                 ("model", LinearSVC())])


def search_C(values):
    grid = GridSearchCV(pipe, {"model__C": values}, cv=5, scoring="f1_macro")
    grid.fit(X_train, y_train)
    macro = f1_score(y_test, grid.predict(X_test), average="macro")
    return [grid.best_params_["model__C"], round(float(macro), 3)]


print(search_C([0.1, 1, 10]))
