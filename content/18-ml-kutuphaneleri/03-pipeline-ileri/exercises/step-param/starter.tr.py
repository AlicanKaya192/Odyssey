from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def step_param(c):
    pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
    pipe.set_params(C=c)
    return [list(pipe.named_steps), pipe["model"].C]

print(step_param(0.1))
