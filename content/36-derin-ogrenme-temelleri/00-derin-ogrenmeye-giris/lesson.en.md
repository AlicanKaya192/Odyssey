# Introduction to Deep Learning

In the machine learning track, most models worked with features that we
prepared: age, income, word counts. **Deep learning** leaves much of that
preparation to the model. The model is a stack of **layers**; each layer
learns a slightly more useful representation from the output of the one
before. This is how we get from raw pixels to "this is a 7", or from raw
sound to words.

In this module we learn the foundations of deep learning with the
**PyTorch** library. In the Neural Networks section of the ML Algorithms
module we built a neural network from scratch with NumPy: the forward pass,
backpropagation with hand-derived derivatives, and the weight update.
PyTorch carries the same idea, but it computes the derivatives **itself**
and gives us ready-made layers. If you have not read that section, that is
fine; we explain every piece from the start here.

## The result first

Before the details, let us see how a deep learning model is trained from
start to finish. The data is the handwritten digits that ship with
scikit-learn: 1797 images of 8×8 pixels each (no internet needed). The task
is to find the digit (0–9) in the image.

```python
import torch
from torch import nn
from sklearn.datasets import load_digits

torch.manual_seed(0)
digits = load_digits()
X = torch.tensor(digits.data, dtype=torch.float32) / 16
y = torch.tensor(digits.target)

model = nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 10))
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(200):
    optimizer.zero_grad()
    loss = loss_fn(model(X[:1200]), y[:1200])
    loss.backward()
    optimizer.step()
    if epoch % 40 == 0:
        print(epoch, round(loss.item(), 2))

correct = (model(X[1200:]).argmax(dim=1) == y[1200:]).sum().item()
print(correct, "/", len(y) - 1200, round(correct / (len(y) - 1200), 2))
```

```text
0 2.33
40 0.48
80 0.2
120 0.13
160 0.1
544 / 597 0.91
```

- We trained on the first 1200 images and tested on the last 597, which
  the model never saw.
- The **loss** measures how wrong the model is. It is 2.33 at
  the start of training and much smaller at the end: the model is learning.
- It got 544 of the 597 unseen digits right.
- The training itself is only four lines: `zero_grad`, the loss,
  `backward`, `step`. The rest of this module opens up each of them.

On this computer the training takes less than a second. We will open up
the code and the numbers one by one through the module; for now, just look
at the whole picture.

## Data: from an image to numbers

A digit image reaches the model as 64 numbers: 8 rows × 8 columns of
pixels, each between 0 (white) and 16 (dark). Let us draw the first image
with characters:

```python
print(digits.data.shape, digits.target[:10].tolist())
for row in digits.images[0]:
    print("".join("#" if v > 6 else "." for v in row))
```

```text
(1797, 64) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
...##...
..####..
..#..##.
..#..##.
..#..##.
..#..##.
..#.##..
...##...
```

This is a 0. In the code, `X = ... / 16` brings the pixel values into the
0–1 range; networks learn more comfortably with small numbers of similar
scale. `torch.tensor` turns a NumPy array into PyTorch's array, a
**tensor**. We look at tensors in detail in the next section.

## The model: layers

`nn.Sequential` connects the layers one after another:

<figure class="fig">
  <div class="flow">
    <span class="node">64 pixels</span><span class="arrow">→</span>
    <span class="node">Linear<br><small>64 → 32</small></span><span class="arrow">→</span>
    <span class="node">ReLU</span><span class="arrow">→</span>
    <span class="node">Linear<br><small>32 → 10</small></span><span class="arrow">→</span>
    <span class="node acc">10 scores</span>
  </div>
  <figcaption>The model's path: 64 numbers go in, one score per digit comes out. The digit with the highest score is the prediction.</figcaption>
</figure>

- `nn.Linear(64, 32)`: a layer that computes 32 outputs from 64 inputs.
  Each output is a weighted sum of the inputs plus a constant. The weights
  and constants are the model's **parameters**; training adjusts them.
- `nn.ReLU()`: a simple function that turns negative numbers into 0.
  Without a non-linear step like this between the layers, two linear layers
  on top of each other would be no different from a single linear layer.
- The last layer gives 10 scores; `argmax` picks the position of the
  highest score, that is, the predicted digit.

Let us give the trained model a few test images:

```python
with torch.no_grad():
    scores = model(X[1200:1208])
print(scores.shape)
print(scores.argmax(dim=1).tolist())
print(y[1200:1208].tolist())
```

```text
torch.Size([8, 10])
[7, 7, 7, 5, 1, 0, 0, 2]
[7, 7, 3, 5, 1, 0, 0, 2]
```

Ten scores for each of eight images, so `8 × 10`. The predictions (second
line) match the true labels (third line) on 7 images.
`torch.no_grad()` means "do not compute derivatives here"; when we only
predict, it saves needless work and memory.

## The training loop: four steps

Every round of the loop (an epoch) does the same four steps:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>optimizer.zero_grad()</code></span><span>Clear the derivatives left from the previous round.</span></div>
    <div class="anat-row"><span><code>loss = loss_fn(model(X), y)</code></span><span>Forward pass: predict and measure the error.</span></div>
    <div class="anat-row"><span><code>loss.backward()</code></span><span>Backpropagation: compute how each parameter affects the loss (its derivative).</span></div>
    <div class="anat-row"><span><code>optimizer.step()</code></span><span>Nudge every parameter in the direction that lowers the loss.</span></div>
  </div>
  <figcaption>The four steps of one training round. These four lines appear everywhere in the module, always in this order.</figcaption>
</figure>

- `loss_fn = nn.CrossEntropyLoss()` is a classification loss: it punishes
  a model that gives a low score to the right digit.
- `torch.optim.SGD(..., lr=0.5)` is **gradient descent**. `lr` is the
  learning rate: how far to move at each step.
- `backward` computes the derivatives by itself; we did not write
  derivatives by hand as in NumPy. This is PyTorch's biggest convenience:
  **automatic differentiation** (autograd).

## Is deep learning always the answer?

Let us give the same data to logistic regression from the machine learning
track:

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=2000).fit(digits.data[:1200], digits.target[:1200])
print((clf.predict(digits.data[1200:]) == digits.target[1200:]).sum())
```

```text
547
```

Logistic regression got 547 images right; our small network
544. The simple model is even a little better: on a small,
clean data set of 64 numbers, deep learning has no advantage. Deep learning
shows its real difference when:

- The data is **raw** and large: high-resolution photos, sound, long text.
  Writing good features by hand is hard; the layers learn the features
  themselves.
- There is a lot of data: thousands or millions of examples. Large networks
  keep improving as the data grows.
- On tabular data (rows and columns), tree-based models (gradient boosting)
  are often still very strong; trying them before moving to deep learning
  is a good habit.

## The path of this module

- **Tensors** and tensor operations: PyTorch's array.
- **Automatic differentiation**: what `backward` does; training the first
  model by hand.
- **nn.Module**, activations, losses, optimisation algorithms.
- **Dataset and DataLoader**: feeding the data in pieces (mini-batches).
- The training loop, overfitting, initialisation and normalisation, the
  learning rate.
- Saving a model, debugging and an end-to-end project.

The models in this track run on the computer's processor (CPU) and are kept
small; every exercise finishes in a few seconds. Large models use a graphics
card (GPU), but the ideas are the same.

## Summary

- Deep learning learns representations from raw data with models that learn
  layer by layer.
- Training in PyTorch: data into tensors, a model with `nn.Sequential`, a
  loss function, an optimizer and a four-step loop.
- A small network learned handwritten digits in under a second; logistic
  regression does well on the same data too. Deep learning's edge is on raw,
  large data.
