The read-only `finetune_tools.py` holds the lesson's data and functions
(`X_old`, `y_old`, `X_new`, `y_new`, `init`, `train`, `accuracy`).
`replay_effect(k, seed)`: build the network with
`rng = np.random.default_rng(seed)` and pre-train it on 0–4
(`train(init([64, 32, 10], rng), X_old[:700], y_old[:700], 500)`). Take 10
examples of every digit of the new task (the lesson's `few`). If `k > 0`,
choose old examples with `rng.choice(700, k, replace=False)` and mix them in.
Fine-tune for 300 steps and return `[new task accuracy, old task accuracy]`
(the test sets are `X_new[400:]` and `X_old[700:]`).

**Expected output:**

```
0 [0.931, 0.065]
50 [0.901, 0.95]
```
