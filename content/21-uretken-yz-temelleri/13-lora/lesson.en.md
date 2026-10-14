# Low-Rank Adaptation (LoRA)

In the previous section we saw two ways of fine-tuning: updating all the
weights (a good result, but everything changes) or only the last layer (cheap,
but not enough). In a model with billions of parameters, updating all the
weights is expensive and means keeping a full copy of the model for every
task. **LoRA** (low-rank adaptation) is a way in between: it freezes the
weights and adds a very small **correction** beside them.

## The idea: the change is low-rank

Fine-tuning turns a weight matrix $W$ into $W + \Delta W$. LoRA's observation
is this: $\Delta W$ is often concentrated in a few directions, that is, it is
**low-rank**. Then we can write it as the product of two thin matrices:

$$\Delta W = A B, \qquad A: d_{\text{in}} \times r, \quad B: r \times d_{\text{out}}$$

For a 64 × 32 layer the full $\Delta W$ is 2048 numbers; with $r = 4$, $A$ and
$B$ together are $4 \times (64 + 32) = 384$ numbers. Let us test the
observation first: we look at the singular values of the change full
fine-tuning made to the first layer in the experiment from 12. The data and
functions from 12 are in the file `finetune_tools.py`.

```python
import numpy as np
from finetune_tools import X_old, y_old, X_new, y_new, init, train, accuracy

pre = train(init([64, 32, 10], np.random.default_rng(0)),
            X_old[:700], y_old[:700], 500)
few = np.concatenate([np.where(y_new[:400] == d)[0][:10]
                      for d in range(5, 10)])
Xf, yf = X_new[few], y_new[few]
full = train(pre, Xf, yf, 300)

delta = full[0][0] - pre[0][0]
S = np.linalg.svd(delta, compute_uv=False)
energy = np.cumsum(S ** 2) / (S ** 2).sum()
for r in [1, 2, 4, 8]:
    print(f"first {r} directions hold {energy[r - 1]:.1%} of the change")
```

```text
first 1 directions hold 32.1% of the change
first 2 directions hold 54.1% of the change
first 4 directions hold 85.2% of the change
first 8 directions hold 99.6% of the change
```

Of the change's 32 possible directions, the first 4 carry 85% of the change
and the first 8 carry 99.6%. So the 64 × 32 change really behaves like an
8-dimensional change. The work that proposed LoRA observed a similar low rank
when fine-tuning large language models too; the small network here only shows
the idea.

## Training LoRA

The first layer's weight $W_1$ stays frozen; the forward pass uses
$W_1 + AB$. $B$ starts at zero, so at the start of training the model is
**exactly** the pre-trained model. Only $A$, $B$ and the last layer are
trained. The derivative of the product $AB$ follows from the chain rule: for
$M = W_1 + AB$, $\partial L / \partial A = (\partial L / \partial M) B^\top$
and $\partial L / \partial B = A^\top (\partial L / \partial M)$.

```python
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
        g_A, g_B = g_M @ B.T, A.T @ g_M
        W2, b2 = W2 - lr * g_W2, b2 - lr * g_b2
        A, B = A - lr * g_A, B - lr * g_B
    return A, B, (W2, b2)


def adapted(pre, A, B, head):
    (W1, b1), _ = pre
    return [(W1 + A @ B, b1), head]


head_only = train(pre, Xf, yf, 300, layers=[1])
results = [("last layer", head_only, 330)]
for r in [1, 2, 4, 8]:
    A, B, head = train_lora(pre, Xf, yf, r)
    results.append((f"LoRA r={r}", adapted(pre, A, B, head),
                    330 + r * (64 + 32)))
results.append(("full", full, 64 * 32 + 32 + 330))
for name, net, params in results:
    print(f"{name:10} accuracy {accuracy(net, X_new[400:], y_new[400:])}",
          f"trained parameters {params}")
```

```text
last layer accuracy 0.802 trained parameters 330
LoRA r=1   accuracy 0.869 trained parameters 426
LoRA r=2   accuracy 0.921 trained parameters 522
LoRA r=4   accuracy 0.94 trained parameters 714
LoRA r=8   accuracy 0.94 trained parameters 1098
full       accuracy 0.931 trained parameters 2410
```

The last layer alone had stopped at 80%. Adding a LoRA with $r = 1$ to it (96
more parameters) raises it to 87%, $r = 2$ to 92%; with $r = 4$ it is 94%, at
the level of full fine-tuning (93%), but with only 714 of the 2410 parameters
full fine-tuning trains. $r = 8$ adds nothing: almost all of the change was
already in the first few directions.

## One seed is not enough

```python
for seed in [0, 1, 2]:
    base = train(init([64, 32, 10], np.random.default_rng(seed)),
                 X_old[:700], y_old[:700], 500)
    A, B, head = train_lora(base, Xf, yf, 4, seed=seed)
    print(seed, "LoRA r=4", accuracy(adapted(base, A, B, head),
                                     X_new[400:], y_new[400:]),
          "full", accuracy(train(base, Xf, yf, 300),
                           X_new[400:], y_new[400:]))
```

```text
0 LoRA r=4 0.94 full 0.931
1 LoRA r=4 0.933 full 0.938
2 LoRA r=4 0.931 full 0.921
```

With three seeds LoRA ($r = 4$) gives 93.1–94% and full fine-tuning
92.1–93.8%: the differences are below one point and change direction. In this
small experiment LoRA is at the same level as full fine-tuning; saying it is
better would need more data.

## It can be attached and detached

LoRA's biggest convenience in practice: the pre-trained model **does not change
at all**. For every task only a small adapter ($A$, $B$ and a new output layer
if needed) is stored; the wanted adapter is attached to the same large model.
Running it need not cost anything extra either: $W_1 + AB$ can be **merged**
into a single matrix.

```python
A, B, head = train_lora(pre, Xf, yf, 4)
merged = pre[0][0] + A @ B
x = X_new[400:]
two_steps = np.tanh(x @ pre[0][0] + x @ A @ B + pre[0][1])
one_step = np.tanh(x @ merged + pre[0][1])
print("merged gives the same output:", np.allclose(two_steps, one_step))
print("old model untouched, old task:",
      accuracy(pre, X_old[700:], y_old[700:]))
print("adapter size vs full copy:", A.size + B.size, "vs", pre[0][0].size)
```

```text
merged gives the same output: True
old model untouched, old task: 1.0
adapter size vs full copy: 384 vs 2048
```

The merged matrix gives the same output; the pre-trained model is still
perfect on the old task, because it was never touched. In large models the
difference is far more striking: for a model with billions of parameters an
adapter can hold only a few million parameters.

## Summary

- The change fine-tuning makes to the weights is often low-rank; in the section
  the first 8 directions carried almost all of the change.
- LoRA adds the product of two thin matrices ($AB$) beside the frozen $W$ and
  trains only them; because $B$ starts at zero, training starts from the
  pre-trained model.
- In the section LoRA with $r = 4$ gave accuracy at the same level as full
  fine-tuning with less than a third of the parameters full fine-tuning trains
  (with all three seeds; the differences below one point).
- The adapter can be attached and detached and merged into the main matrix; the
  pre-trained model does not change.
