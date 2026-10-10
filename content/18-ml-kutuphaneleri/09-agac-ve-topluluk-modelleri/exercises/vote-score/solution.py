from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def vote_score(weights):
    base = [("lr", make_pipeline(StandardScaler(), LogisticRegression())),
            ("rf", RandomForestClassifier(n_estimators=100, random_state=0))]
    vote = VotingClassifier(base, voting="soft", weights=weights)
    return round(float(cross_val_score(vote, X_train, y_train, cv=5).mean()), 3)

print(vote_score([1, 1]))
print(vote_score([1, 3]))
