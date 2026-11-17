# Activation and Loss Functions

In a neural network we choose two kinds of functions. **Activations** go
between the layers and give the network a non-linear step. **Loss
functions** compare the network's output with the true answer and give the
single number training tries to make small. In this section we look at both
and open up the most commonly confused topic: the difference between the
model's raw output (**logits**) and probabilities (**softmax**).

## Activations

Let us apply the three most common activations to the same numbers:

```python
import torch
from torch import nn

z = torch.tensor([-2.0, -0.5, 0.0, 0.5, 2.0])
for name, fn in [("relu", torch.relu), ("sigmoid", torch.sigmoid), ("tanh", torch.tanh)]:
    print(name, [round(v, 3) for v in fn(z).tolist()])
```

```text
relu [0.0, 0.0, 0.0, 0.5, 2.0]
sigmoid [0.119, 0.378, 0.5, 0.622, 0.881]
tanh [-0.964, -0.462, 0.0, 0.462, 0.964]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>ReLU</span><span><code>max(0, z)</code>. The default choice in hidden layers: simple, fast, its gradient is always 1 on the positive side.</span></div>
    <div class="anat-row"><span>Sigmoid</span><span>Squeezes every number between 0 and 1. Used to turn the output into a probability in binary classification.</span></div>
    <div class="anat-row"><span>Tanh</span><span>Squeezes between −1 and 1, symmetric around 0. Common in recurrent networks.</span></div>
  </div>
  <figcaption>Three activations and where they are used.</figcaption>
</figure>

Sigmoid and tanh **saturate** on large numbers: whether the input is 5 or
50, the output is almost the same and the gradient almost zero. In deep
networks the gradient flows back multiplied through the layers, so
saturating activations slow learning down; that is why ReLU is preferred in
hidden layers.

## Why is an activation needed?

Two linear layers without an activation are no different from a single
linear layer:

```python
torch.manual_seed(0)
first = nn.Linear(4, 8, bias=False)
second = nn.Linear(8, 3, bias=False)
x = torch.randn(5, 4)
combined = second.weight @ first.weight
print(combined.shape, torch.allclose(second(first(x)), x @ combined.T, atol=1e-6))
```

```text
torch.Size([3, 4]) True
```

The weights of the two layers can be replaced by a single `(3, 4)` matrix: no
matter how many layers you add, the network still draws a line (a plane). A
ReLU in between breaks this product and gives the network the power to draw
curved boundaries.

## Logits and softmax

The last layer of a classification network gives a **raw score** for each
class. These are called **logits**: they can be any real number and do not
sum to 1. To turn them into probabilities we apply **softmax**:
`softmax(z)ᵢ = exp(zᵢ) / Σ exp(zⱼ)`.

```python
logits = torch.tensor([[2.0, 1.0, 0.1], [0.5, 2.5, -1.0]])
probs = torch.softmax(logits, dim=1)
print([[round(v, 3) for v in row] for row in probs.tolist()])
print([round(v, 4) for v in probs.sum(dim=1).tolist()])
print(logits.argmax(dim=1).tolist(), probs.argmax(dim=1).tolist())
```

```text
[[0.659, 0.242, 0.099], [0.116, 0.858, 0.026]]
[1.0, 1.0]
[0, 1] [0, 1]
```

- Softmax turned each row into probabilities that sum to 1; a large logit
  gives a large probability.
- It does not change the order: the `argmax` of the logits equals the
  `argmax` of the probabilities. **If you only need the prediction, you do
  not need softmax.**

<figure class="fig">
  <div class="flow">
    <span class="node">Input</span><span class="arrow">→</span>
    <span class="node">Layers</span><span class="arrow">→</span>
    <span class="node acc">Logits<br><small>raw scores</small></span><span class="arrow">→</span>
    <span class="node">softmax<br><small>only if probabilities are needed</small></span>
  </div>
  <figcaption>The model's output is logits. The loss function takes logits too; we apply softmax at the end, only to show probabilities.</figcaption>
</figure>

## `CrossEntropyLoss` wants logits

The loss of multi-class classification is **cross-entropy**: minus the log
of the right class's probability. PyTorch's `nn.CrossEntropyLoss` does the
softmax **itself**; you give it logits:

```python
targets = torch.tensor([0, 1])
loss_fn = nn.CrossEntropyLoss()
by_hand = -torch.log(probs[torch.arange(2), targets]).mean()
print(round(loss_fn(logits, targets).item(), 4), round(by_hand.item(), 4))
print(round(loss_fn(probs, targets).item(), 4))
```

```text
0.2851 0.2851
0.725
```

- The first two numbers match: `CrossEntropyLoss(logits)` = softmax + minus
  log + mean.
- The third is the wrong use: giving probabilities. The loss is still
  computed and **raises no error**, but softmax has been applied twice and
  the number is different. A model trained this way seems to train but
  learns worse (the first note shows why).

The rule: **no softmax in the model's last layer**; the loss takes logits.
For a prediction use `argmax(logits)`; to show probabilities use
`torch.softmax(logits, dim=1)`.

## Binary classification: sigmoid and `BCEWithLogitsLoss`

For two classes the output can be a single logit; sigmoid turns it into
"the probability of being 1". The loss is binary cross-entropy. Here too
the version that takes logits is recommended:

```python
z = torch.tensor([1.5, -0.5, 3.0])
target = torch.tensor([1.0, 0.0, 0.0])
with_logits = nn.BCEWithLogitsLoss()(z, target)
two_steps = nn.BCELoss()(torch.sigmoid(z), target)
print(round(with_logits.item(), 4), round(two_steps.item(), 4))
```

```text
1.2414 1.2414
```

Both give the same result. `BCEWithLogitsLoss` merges the sigmoid and the
logarithm into one formula, so it is numerically safe even for very large or
very small logits. The targets here are **decimals** (`1.0`, `0.0`); in
`CrossEntropyLoss` they are class numbers (`int64`).

## Regression losses

For predicting numbers there are two basic losses: the mean squared error
(`MSELoss`) and the mean absolute error (`L1Loss`). Their difference shows up
with an **outlier**:

```python
pred = torch.tensor([2.0, 3.0, 4.0, 5.0])
clean = torch.tensor([2.5, 3.0, 3.5, 5.0])
outlier = torch.tensor([2.5, 3.0, 3.5, 25.0])
for name, fn in [("mse", nn.MSELoss()), ("l1", nn.L1Loss())]:
    print(name, fn(pred, clean).item(), fn(pred, outlier).item())
```

```text
mse 0.125 100.125
l1 0.25 5.25
```

A single outlier multiplies the MSE by 801, because the square
of an error of 20 is 400. L1 grows only 21 times. On data with
many outliers, L1 (or `SmoothL1Loss`, in between the two) gives a calmer
training.

## Summary

- ReLU in hidden layers; layers without activations collapse into one linear
  layer.
- The model's raw output is **logits**; softmax turns it into probabilities
  but does not change the order.
- `CrossEntropyLoss` wants logits and class numbers; do not put a softmax in
  the last layer.
- For binary classification, `BCEWithLogitsLoss` with decimal targets.
- In regression, MSE is very sensitive to outliers, L1 less so.
