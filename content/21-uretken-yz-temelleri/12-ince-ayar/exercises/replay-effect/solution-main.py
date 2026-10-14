import numpy as np
from finetune_tools import X_old, y_old, X_new, y_new, init, train, accuracy


def replay_effect(k, seed):
    rng = np.random.default_rng(seed)
    base = train(init([64, 32, 10], rng), X_old[:700], y_old[:700], 500)
    few = np.concatenate([np.where(y_new[:400] == d)[0][:10] for d in range(5, 10)])
    Xs, ys = X_new[few], y_new[few]
    if k > 0:
        pick = rng.choice(700, k, replace=False)
        Xs, ys = np.concatenate([Xs, X_old[pick]]), np.concatenate([ys, y_old[pick]])
    net = train(base, Xs, ys, 300)
    return [accuracy(net, X_new[400:], y_new[400:]), accuracy(net, X_old[700:], y_old[700:])]


for k in [0, 50]:
    print(k, replay_effect(k, 0))
