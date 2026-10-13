# Text Classification with a Neural Network

In NLP Fundamentals we classified reviews with TF-IDF and linear models. In
this section we do the same job with a small **neural network**: an
**embedding layer** that turns words into embeddings, the average of the
embeddings, a hidden layer and an output that gives probabilities. This time
we do not build the embeddings beforehand; the network learns them itself,
**for the task**. We write the whole forward and backward computation by hand
with NumPy; it is the neural network of section 20 of the ML Algorithms
module, adapted to text.

## From words to numbers

We give each word an index; words not seen in training become 0 (unknown).
The split is the same as in NLP Fundamentals.

```python
import re

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_reviews

TOKEN = re.compile(r"[a-z']+")
reviews = make_reviews(2000)
classes = ["negative", "neutral", "positive"]
texts = [r["text"] for r in reviews]
y_all = np.array([classes.index(r["label"]) for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, y_all, test_size=0.25, random_state=0, stratify=y_all)
vocab = sorted({w for t in X_train for w in TOKEN.findall(t.lower())})
index = {w: i + 1 for i, w in enumerate(vocab)}
V = len(vocab) + 1


def to_ids(text):
    return [index.get(w, 0) for w in TOKEN.findall(text.lower())] or [0]


def averaging(texts):
    A = np.zeros((len(texts), V))
    for row, text in enumerate(texts):
        ids = to_ids(text)
        for i in ids:
            A[row, i] += 1 / len(ids)
    return A


A_train, A_test = averaging(X_train), averaging(X_test)
print(V, A_train.shape, to_ids("The lid is great")[:4])
```

```text
308 (1500, 308) [253, 151, 144, 131]
```

`averaging` builds one row per text: `1/length` in the places of its words.
Multiplying this row by the embedding table (`A @ E`) gives the **average**
of the text's word embeddings. Writing the average as a matrix product lets
us take the derivative of the embedding table in the backward pass with a
single product too.

## The forward pass

The layers of the network:

1. `x = A @ E`: the text's average embedding (16 numbers)
2. `h = ReLU(x @ W1 + b1)`: a hidden layer of 32 neurons
3. `p = softmax(h @ W2 + b2)`: the probabilities of the three classes

```python
rng = np.random.default_rng(0)
params = {"E": rng.normal(0, 0.1, (V, 16)),
          "W1": rng.normal(0, np.sqrt(2 / 16), (16, 32)), "b1": np.zeros(32),
          "W2": rng.normal(0, np.sqrt(1 / 32), (32, 3)), "b2": np.zeros(3)}


def forward(P, A):
    x = A @ P["E"]
    h = np.maximum(x @ P["W1"] + P["b1"], 0)
    z = h @ P["W2"] + P["b2"]
    z = z - z.max(axis=1, keepdims=True)
    p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
    return x, h, p


def loss(P, A, y):
    p = forward(P, A)[2]
    return float(-np.log(p[np.arange(len(y)), y]).mean())


print(forward(params, A_train[:2])[2].round(3))
print(round(loss(params, A_train, y_train), 3), round(np.log(3), 3))
```

```text
[[0.335 0.326 0.339]
 [0.334 0.336 0.329]]
1.102 1.099
```

Before training the probabilities are close to a third and the loss is
around `log 3 ≈ 1.099`: the network knows nothing. Subtracting the largest
value before softmax prevents numerical overflow and does not change the
result.

## The backward pass and a gradient check

With the chain rule we derive the derivative of every parameter. A
hand-written derivative is easy to get wrong; so we compare it with a
**numerical derivative**: nudge a parameter by `ε` and measure the change in
the loss.

```python
def backward(P, A, y):
    x, h, p = forward(P, A)
    g = p.copy()
    g[np.arange(len(y)), y] -= 1
    g /= len(y)
    grads = {"W2": h.T @ g, "b2": g.sum(axis=0)}
    gh = g @ P["W2"].T
    gh[h <= 0] = 0
    grads["W1"], grads["b1"] = x.T @ gh, gh.sum(axis=0)
    grads["E"] = A.T @ (gh @ P["W1"].T)
    return grads


A, y = A_train[:50], y_train[:50]
grads = backward(params, A, y)
for name, pos in [("W2", (0, 0)), ("E", (index["great"], 3))]:
    eps = 1e-5
    params[name][pos] += eps
    up = loss(params, A, y)
    params[name][pos] -= 2 * eps
    down = loss(params, A, y)
    params[name][pos] += eps
    numeric = (up - down) / (2 * eps)
    print(name, f"{grads[name][pos]:.6f}", f"{numeric:.6f}")
```

```text
W2 0.003604 0.003604
E 0.000095 0.000095
```

- The derivative we derived by hand and the numerical one agree to six
  places. The backward pass is correct.
- The derivative of softmax + cross-entropy at the output is very simple:
  `p − y` (subtract 1 from the right class's probability).
- The derivative of the embedding table is `A.T @ ...`: only the rows of
  words appearing in the text are updated.

## Training

```python
def predict(P, A):
    return forward(P, A)[2].argmax(axis=1)


rng = np.random.default_rng(1)
for epoch in range(1, 31):
    order = rng.permutation(len(y_train))
    for start in range(0, len(order), 32):
        batch = order[start:start + 32]
        grads = backward(params, A_train[batch], y_train[batch])
        for name in params:
            params[name] -= 0.5 * grads[name]
    if epoch % 10 == 0:
        accuracy = (predict(params, A_test) == y_test).mean()
        print(epoch, round(loss(params, A_train, y_train), 3), round(float(accuracy), 3))
```

```text
10 0.169 0.87
20 0.135 0.878
30 0.113 0.866
```

Test accuracy rises to about 87%: in NLP Fundamentals TF-IDF + logistic
regression reached 88%. The network has about 5600 parameters (`308 × 16 + 16
× 32 + 32 × 3` weights and 35 biases). While the training loss keeps
falling, test accuracy drops from 0.878 at epoch 20 to 0.866 at epoch 30: the
network may have started to memorise the training data (overfitting).
Stopping training by watching validation data (early stopping) prevents
this.

## Which words does the network rely on?

Looking at the rows of the embedding layer one by one says little; they carry
meaning together with the hidden layer. Let us ask a clearer question: what
does the network say when given each word **alone**? Let `positive −
negative` probability be the word's "lean":

```python
probs = forward(params, averaging(vocab))[2]
lean = probs[:, 2] - probs[:, 0]
order = np.argsort(lean)
print("negative", [vocab[i] for i in order[:6]])
print("positive", [vocab[i] for i in order[::-1][:6]])
for word in ["good", "bad", "great", "not"]:
    print(word, round(float(lean[vocab.index(word)]), 3))
```

```text
negative ['not', 'hate', 'awful', 'terrible', 'i', 'just']
positive ['much', 'totally', 'better', 'well', 'excellent', 'fantastic']
good 1.0
bad 1.0
great -0.971
not -1.0
```

- At the negative end are "not", "hate", "awful", "terrible"; at the positive
  end "excellent", "fantastic", "better". As expected.
- But "great" is **negative** (−0.97). In the data, ironic sentences such as
  "Great, the lid broke on day 3" appear in negative reviews; the network
  learned "great" as a negative signal. The "just" at the negative end comes
  from the pattern "Just perfect, the strap is weak again".
- "bad" alone is **positive** (+1.0): "not bad" appears in positive reviews,
  and the negativity is carried by the word "not".
- The network did not learn a sentiment lexicon; it learned **the signals in
  this data**. Every model learned from labelled data does this (shortcut
  learning). Looking at which words a model relies on (like `coef_` in 09) is
  the way to catch these surprises.

## The limit of the average

```python
for text in ["good", "not good at all", "bad", "not bad at all"]:
    print(text, classes[predict(params, averaging([text]))[0]])
```

```text
good positive
not good at all negative
bad positive
not bad at all negative
```

An average is a bag: the only difference between "not good" and "good" is the
vector of "not". "good" is positive and "not good at all" negative: right.
But "bad" is positive and "not bad at all" negative: both wrong. The network
counts "not" as a negative signal everywhere; it does not know what "not"
negates, because it does not see order. For a network that can process word
order we move on to recurrent neural networks (RNNs) in the next section.

## Summary

- A simple neural network that classifies text: embedding layer → average →
  hidden layer → softmax.
- The backward pass was written by hand with the chain rule and checked
  against a numerical derivative.
- Test accuracy is about 87%, close to TF-IDF + logistic regression.
- The network learned the signals of this data: "great" is negative because
  of ironic patterns, "bad" positive because of "not bad". The average does
  not see order.
