import numpy as np
from finetune_tools import X_old, y_old, X_new, y_new, init, train, accuracy


def replay_effect(k, seed):
    return [0.0, 0.0]


for k in [0, 50]:
    print(k, replay_effect(k, 0))
