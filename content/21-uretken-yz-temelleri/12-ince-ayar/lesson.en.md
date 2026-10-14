# Fine-Tuning and Alignment

A large language model first goes through **pre-training** on a very large
amount of text (the NLP path's Pre-trained Models section); it learns to
predict the next token. To become a chat assistant it needs two more steps:
**instruction tuning** and **preference alignment**. This section measures the
ideas beneath both with small NumPy experiments: what fine-tuning is, what it
breaks, and how a model is steered towards the answers "people prefer".

## Fine-tuning: continuing training where it stopped

**Fine-tuning** is training a pre-trained model's weights a little more with a
new task's data. Let us set up a small experiment: we train a 64 → 32 → 10
network only on the **0–4** images of the 8×8 digits (this network is the
"pre-trained model"). Then a new task arrives: recognising the digits **5–9**,
but there are only 10 examples of each.

```python
import numpy as np
from gen_data import load_digit_images

X, y = load_digit_images()
y = np.array(y)
order = np.random.default_rng(0).permutation(len(X))
X, y = X[order], y[order]
X_old, y_old = X[y < 5], y[y < 5]
X_new, y_new = X[y >= 5], y[y >= 5]


def init(sizes, rng):
    return [(rng.normal(0, np.sqrt(1 / a), (a, b)), np.zeros(b))
            for a, b in zip(sizes, sizes[1:])]


def forward(x, net):
    acts = [x]
    for i, (W, b) in enumerate(net):
        z = acts[-1] @ W + b
        if i < len(net) - 1:
            acts.append(np.tanh(z))
        else:
            e = np.exp(z - z.max(axis=1, keepdims=True))
            acts.append(e / e.sum(axis=1, keepdims=True))
    return acts


def train(net, X, y, steps, lr=0.5, layers=None):
    net = [(W.copy(), b.copy()) for W, b in net]
    layers = range(len(net)) if layers is None else layers
    onehot = np.eye(10)[y]
    for _ in range(steps):
        acts = forward(X, net)
        grad = (acts[-1] - onehot) / len(X)
        for i in reversed(range(len(net))):
            W, b = net[i]
            gW, gb = acts[i].T @ grad, grad.sum(axis=0)
            if i:
                grad = grad @ W.T * (1 - acts[i] ** 2)
            if i in layers:
                net[i] = (W - lr * gW, b - lr * gb)
    return net


def accuracy(net, X, y):
    return round(float((forward(X, net)[-1].argmax(1) == y).mean()), 3)


pre = train(init([64, 32, 10], np.random.default_rng(0)),
            X_old[:700], y_old[:700], 500)
print("old task", accuracy(pre, X_old[700:], y_old[700:]))
```

```text
old task 1.0
```

The pre-trained network is almost perfect on the old task (0–4). Now let us
fine-tune it in two ways with the new task's 50 examples: updating **all the
weights**, and updating only the **last layer** (with the layer below frozen).

```python
few = np.concatenate([np.where(y_new[:400] == d)[0][:10]
                      for d in range(5, 10)])
Xf, yf = X_new[few], y_new[few]
full = train(pre, Xf, yf, 300)
head = train(pre, Xf, yf, 300, layers=[1])
for name, net in [("full", full), ("last layer", head)]:
    print(f"{name:10} new task {accuracy(net, X_new[400:], y_new[400:])}",
          f"old task {accuracy(net, X_old[700:], y_old[700:])}")
```

```text
full       new task 0.931 old task 0.065
last layer new task 0.802 old task 0.189
```

Fine-tuning all the weights reached 93% on the new task; the last layer alone
stopped at 80%: the intermediate features learnt for 0–4 are not quite enough
to separate 5–9. But the price is high: after fine-tuning the network fell to
6.5% on the old task and recognises almost none of the digits 0–4. This is
called **catastrophic forgetting**: since the new data has no example of the
old task, the model has no reason to keep it. Training only the last layer
also makes it forget (19%), because the output layer now learns to give only
the answers 5–9.

## The cure for forgetting: mix in the old as well

Mixing a few examples of the old task into the fine-tuning data (**replay**)
lets the model keep the old task too. Let us repeat the same experiment with
three seeds, adding 50 old examples to the 50 new ones:

```python
for seed in [0, 1, 2]:
    rng = np.random.default_rng(seed)
    base = train(init([64, 32, 10], rng), X_old[:700], y_old[:700], 500)
    replay = rng.choice(700, 50, replace=False)
    Xm = np.concatenate([Xf, X_old[replay]])
    ym = np.concatenate([yf, y_old[replay]])
    only_new, mixed = train(base, Xf, yf, 300), train(base, Xm, ym, 300)
    print(seed, "only new:", accuracy(only_new, X_new[400:], y_new[400:]),
          accuracy(only_new, X_old[700:], y_old[700:]),
          "| mixed:", accuracy(mixed, X_new[400:], y_new[400:]),
          accuracy(mixed, X_old[700:], y_old[700:]))
```

```text
0 only new: 0.931 0.065 | mixed: 0.901 0.95
1 only new: 0.938 0.055 | mixed: 0.893 0.98
2 only new: 0.921 0.045 | mixed: 0.865 0.945
```

With only new data, the old task's accuracy is 4.5–6.5% with all three seeds.
Mixing in 50 old examples keeps it at 94.5–98%. The price is a few points on
the new task (from 92–94% to 86.5–90%): the network's capacity is now shared
between two tasks.

## Instruction tuning

A pre-trained language model continues text but does not know a task like
"answer the question". **Instruction tuning** trains the model on thousands
of (instruction, good answer) pairs:

```text
{"instruction": "Summarise the return policy in one sentence.",
 "response": "You can return unused items within 30 days of delivery."}
{"instruction": "Is shipping free for a 30 euro order?",
 "response": "No. Shipping is free only over 50 euros."}
```

The model learns the form in this data: answering an instruction, writing at
the requested length, saying so when something is not in the source. The
lesson of the experiment above holds here too: training only on new data can
wear down the model's earlier skills; that is why general-purpose examples are
mixed into the fine-tuning data as well.

## A reward model from preferences

Writing down that an answer is "good" is hard, but saying which of two answers
is better is easy. That is why **preference alignment** learns from pairwise
comparisons. First a **reward model** is built: it gives every answer a score
$r$, and the probability that "a is preferred to b" is $\sigma(r(a) - r(b))$
(the Bradley–Terry model).

Let us see this with synthetic data. We describe every answer with three
features: is it correct (0/1), does it cite a source (0/1), its length
(0.2–2.0). A rule acting like a labeller makes preferences on 400 pairs with
hidden weights (`TRUE_W`: correctness 3, source 1, length −0.5) and some
randomness. We learn the reward model from these preferences alone:

```python
def features(rng, n):
    return np.column_stack([rng.integers(0, 2, n), rng.integers(0, 2, n),
                            rng.uniform(0.2, 2.0, n)])


def preferences(F, weights, rng, n_pairs=400):
    pairs = rng.integers(0, len(F), (n_pairs, 2))
    pairs = pairs[pairs[:, 0] != pairs[:, 1]]
    diff = F[pairs[:, 0]] - F[pairs[:, 1]]
    first = rng.random(len(pairs)) < 1 / (1 + np.exp(-diff @ weights))
    return np.where(first[:, None], diff, -diff)


def fit_reward(D, steps=2000, lr=0.5):
    w = np.zeros(D.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-D @ w))
        w += lr * D.T @ (1 - p) / len(D)
    return w


rng = np.random.default_rng(0)
TRUE_W = np.array([3.0, 1.0, -0.5])
answers = features(rng, 300)
w = fit_reward(preferences(answers, TRUE_W, rng))
print("learned", w.round(2), "hidden", TRUE_W)
```

```text
learned [ 2.63  1.31 -0.72] hidden [ 3.   1.  -0.5]
```

`preferences` returns every pair as the feature difference "preferred − not
preferred"; `fit_reward` finds the weights that raise the probability of these
differences with gradient ascent (logistic regression). The learnt weights are
close to the hidden ones: the model worked out what the labeller rewards from
the preferences alone.

## Choosing with the reward

Once there is a reward model, the simplest use is: produce several answers to
the same question and choose the one with the highest reward (**best-of-n**).
Real alignment methods (reinforcement learning or direct preference training)
train the model towards producing high-reward answers; the idea is the same.

```python
candidates = features(rng, 8000).reshape(1000, 8, 3)
best = candidates[np.arange(1000), (candidates @ w).argmax(axis=1)]
print("correct: first answer", candidates[:, 0, 0].mean().round(3),
      "best of 8", best[:, 0].mean().round(3))
```

```text
correct: first answer 0.497 best of 8 0.993
```

The first answer is correct 50% of the time (at random); choosing from 8
answers with the reward model gives 99%. The model itself did not change; the
answers improved only by choosing. The price is 8 times the generation.

## Fooling the reward

A reward model learns the labellers' preferences; **their mistakes too**. What
happens if the labellers struggle to check correctness and like long,
detailed-looking answers (hidden weights: correctness 0.5, source 0.2, length
1.5)?

```python
BIASED_W = np.array([0.5, 0.2, 1.5])
w_biased = fit_reward(preferences(answers, BIASED_W, rng))
picked = candidates[np.arange(1000), (candidates @ w_biased).argmax(axis=1)]
print("learned", w_biased.round(2))
print("best of 8: correct", picked[:, 0].mean().round(3),
      "length", picked[:, 2].mean().round(2),
      "| first answer length", candidates[:, 0, 2].mean().round(2))
```

```text
learned [0.56 0.31 1.6 ]
best of 8: correct 0.776 length 1.75 | first answer length 1.09
```

The reward model faithfully learnt the labellers' bias: the weight of length is
1.6. The answers chosen with the reward have an average length of 1.75 (1.09
for the first answers) and are correct 78% of the time: better than random,
but far below the 99% chosen with the right reward. Pushing the reward to the
top raised what the reward measures (length), not what is wanted
(correctness). This is called **reward hacking**. Needlessly long,
confident-looking answers are a commonly reported example in real models too;
that is why preference data is collected carefully and an aligned model is
also evaluated with measures independent of the reward.

## Summary

- Fine-tuning: continuing to train a pre-trained model with new data; all the
  weights or only some of them are updated.
- Fine-tuning on new data alone can make the model forget the old task (in the
  section accuracy fell from ~1.0 to ~0.05); mixing in part of the old data
  largely prevented this.
- Instruction tuning teaches the model to "answer the question" with
  (instruction, good answer) pairs.
- Preference alignment learns a reward model from pairwise comparisons and
  steers the model towards high-reward answers.
- A reward model also learns the labellers' biases; raising the reward does not
  always improve the answer.
