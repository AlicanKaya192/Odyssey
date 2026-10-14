import numpy as np
from finetune_tools import X_old, y_old, X_new, y_new, init, train, accuracy

pre = train(init([64, 32, 10], np.random.default_rng(0)), X_old[:700], y_old[:700], 500)
few = np.concatenate([np.where(y_new[:400] == d)[0][:10] for d in range(5, 10)])
Xf, yf = X_new[few], y_new[few]


def train_lora(pre, X, y, r, steps=300, lr=0.5, seed=0):
    rng = np.random.default_rng(seed)
    (W1, b1), (W2, b2) = pre
    A, B = rng.normal(0, 0.01, (64, r)), np.zeros((r, 32))
    W2, b2 = W2.copy(), b2.copy()
    onehot = np.eye(10)[y]
    for _ in range(steps):
        h = np.tanh(X @ (W1 + A @ B) + b1)
        z = h @ W2 + b2
        e = np.exp(z - z.max(axis=1, keepdims=True))
        grad = (e / e.sum(axis=1, keepdims=True) - onehot) / len(X)
        g_W2, g_b2 = h.T @ grad, grad.sum(axis=0)
        g_M = X.T @ (grad @ W2.T * (1 - h ** 2))
        # TODO: A ve B'nin turevleri (dersteki zincir kurali).
        g_A, g_B = 0 * A, 0 * B
        W2, b2 = W2 - lr * g_W2, b2 - lr * g_b2
        A, B = A - lr * g_A, B - lr * g_B
    return A, B, (W2, b2)


def lora_accuracy(r):
    A, B, head = train_lora(pre, Xf, yf, r)
    (W1, b1), _ = pre
    return accuracy([(W1 + A @ B, b1), head], X_new[400:], y_new[400:])


print(lora_accuracy(4))
