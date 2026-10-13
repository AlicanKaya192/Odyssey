# The Transformer Block

In 2017 the paper "Attention Is All You Need" (Vaswani and colleagues) left
the RNN behind completely: instead of reading the text step by step, all the
words attend to each other **at the same time**. This structure is called
the **transformer**, and today's large language models are all built by
stacking transformer blocks. In this section we build one block piece by
piece with NumPy: self-attention, position information, the causal mask,
multi-head attention, layer normalisation and residual connections. The
weights are random; the goal is to see what the block does and why it is
built this way.

## Self-attention

In 10 there was a single query. In **self-attention** every word produces
its own query, key and value with three separate weight matrices: `Q = X Wq`,
`K = X Wk`, `V = X Wv`. Then every word attends to all the words; the scores
form an `n × n` table.

```python
import numpy as np

rng = np.random.default_rng(0)
words = ["the", "dog", "chased", "the", "cat"]
vocab = sorted(set(words))
d = 16
E = rng.normal(0, 1, (len(vocab), d))
X = E[[vocab.index(w) for w in words]]
Wq, Wk, Wv = (rng.normal(0, d ** -0.5, (d, d)) for _ in range(3))


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def self_attention(X, mask=None):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    scores = Q @ K.T / np.sqrt(d)
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    A = softmax(scores)
    return A @ V, A


out, A = self_attention(X)
print(X.shape, out.shape, A.shape)
print(A.round(2))
```

```text
(5, 16) (5, 16) (5, 5)
[[0.11 0.14 0.14 0.11 0.49]
 [0.05 0.52 0.33 0.05 0.05]
 [0.26 0.11 0.19 0.26 0.18]
 [0.11 0.14 0.14 0.11 0.49]
 [0.44 0.04 0.02 0.44 0.06]]
```

- Each row is one word's attention weights, summing to 1. The output has
  the same size as the input: 16 numbers per word, but now carrying a mix of
  the other words.
- The first and fourth rows are the same: both are "the". This hints at a
  problem.

## Where is the order?

"the dog chased the cat" and "the cat chased the dog" are not the same
thing. Let us swap the words:

```python
order = [0, 4, 2, 3, 1]
out2, _ = self_attention(X[order])
print(np.allclose(out2, out[order]))
print(np.allclose(out[0], out[3]))
```

```text
True
True
```

- Changing the order only changes where the outputs are; each word's output
  is the same. Self-attention does **not see** order: it treats the words
  like a set. It does not know whether "dog" is chasing or being chased.
- The same word gives the same output everywhere.

## Positional encoding

The fix is to **add** a vector specific to each position to the word's
embedding. The transformer paper used sine and cosine waves turning at
different speeds: low dimensions change fast, high dimensions slowly.

```python
def positions(n, d):
    pos = np.arange(n)[:, None]
    angle = pos / 10000 ** (np.arange(0, d, 2) / d)
    P = np.zeros((n, d))
    P[:, 0::2], P[:, 1::2] = np.sin(angle), np.cos(angle)
    return P


Pe = positions(5, d)
a, _ = self_attention(X + Pe)
b, _ = self_attention(X[order] + Pe)
print(np.allclose(b, a[order]), np.allclose(a[0], a[3]))
Pl = positions(60, 64)
cos = [Pl[10] @ Pl[10 + k] / 32 for k in [0, 1, 2, 5, 10, 20, 40]]
print([round(float(c), 2) for c in cos])
```

```text
False False
[1.0, 0.97, 0.88, 0.73, 0.66, 0.59, 0.48]
```

- With positions added, changing the order really changes the output, and
  the two "the"s are now different.
- The last line is the similarity (cosine) of the 64-dimensional vector of
  position 10 with those 0, 1, 2, 5, 10, 20, 40 steps further on: nearby
  positions are more similar. The model can read "are these two words next
  to each other or far apart" from this.
- Most of today's models learn their position vectors or use relative
  position methods; the idea is the same: order must be given to attention
  separately.

## The causal mask

A language model predicts the next word; if during training a word saw the
words **after** it, it would copy the answer. A **causal mask** lets each
word look only at itself and the words before it: the part of the score
table above the diagonal is set to `-inf`, and softmax gives zero there.

```python
mask = np.tril(np.ones((5, 5), dtype=bool))
_, A = self_attention(X + Pe, mask)
print(A.round(2))
```

```text
[[1.   0.   0.   0.   0.  ]
 [0.17 0.83 0.   0.   0.  ]
 [0.5  0.14 0.37 0.   0.  ]
 [0.22 0.29 0.3  0.19 0.  ]
 [0.66 0.09 0.03 0.21 0.01]]
```

- The table is lower triangular: the first word looks only at itself
  (weight 1), the last word at all of them.
- Thanks to the mask, the "next word" predictions for all the positions of a
  sentence are computed **at once, in parallel**; there is no need to wait
  in turn as in an RNN (the second note).

## Multi-head attention and the block

A single attention asks a single "question". **Multi-head attention** splits
the vector into pieces and runs a separate attention on each piece: one head
can look at the subject, another at the nearby word. The results are joined
and mixed by a matrix (`Wo`). The rest of the block:

- **Layer normalisation**: scales each word's vector to mean 0 and standard
  deviation 1.
- **Feed-forward network**: a two-layer network applied to each word
  separately; its width is usually `4d`.
- **Residual connection**: each sublayer's output is **added** to its input
  (`X + f(X)`).

```python
heads = 4
Wo = rng.normal(0, d ** -0.5, (d, d))
W1 = rng.normal(0, d ** -0.5, (d, 4 * d))
W2 = rng.normal(0, (4 * d) ** -0.5, (4 * d, d))


def layer_norm(x):
    mu, var = x.mean(axis=-1, keepdims=True), x.var(axis=-1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5)


def multi_head(X, mask):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    size = d // heads
    outs = []
    for h in range(heads):
        s = slice(h * size, (h + 1) * size)
        scores = Q[:, s] @ K[:, s].T / np.sqrt(size)
        outs.append(softmax(np.where(mask, scores, -np.inf)) @ V[:, s])
    return np.concatenate(outs, axis=1) @ Wo


def block(X, mask):
    X = X + multi_head(layer_norm(X), mask)
    return X + np.maximum(layer_norm(X) @ W1, 0) @ W2


Y = block(X + Pe, mask)
N = layer_norm(Y)
print(Y.shape, np.allclose(N.mean(axis=1), 0), N.std(axis=1).round(3))
```

```text
(5, 16) True [1. 1. 1. 1. 1.]
```

- The block gives an output of the same size as its input, so blocks can be
  stacked as many as we like. Real models have 12, 32, 80 blocks.
- Each head works on a 4-dimensional piece: the total cost of four heads is
  the same as a single 16-dimensional attention.
- This arrangement, putting the norm at the sublayer's **input** (pre-norm),
  is the most common today; the original paper applied the norm after the
  addition.

## How many parameters?

A block has the four attention matrices (`Wq`, `Wk`, `Wv`, `Wo`: `4d²`), the
feed-forward network's two matrices (`2 × 4d²`) and the scale and shift
values of the two layer norms (`4d`). We do not count bias terms.

```python
def block_params(d):
    return 4 * d * d + 2 * 4 * d * d + 4 * d


for d_model, layers in [(16, 1), (768, 12), (4096, 32)]:
    print(d_model, layers, f"{layers * block_params(d_model):,}")
```

```text
16 1 3,136
768 12 84,971,520
4096 32 6,442,975,232
```

- Our block has 3136 parameters. A model with 768 dimensions and 12 blocks
  carries about 85 million in its blocks, one with 4096 dimensions and 32
  blocks 6.4 billion. The vocabulary's embedding table is added to these.
- The parameter count grows with `d²`: doubling the size makes the block four
  times bigger.

## Summary

- Self-attention: each word produces `Q`, `K`, `V` and attends to all the
  words; an `n × n` table.
- Attention does not see order; positional encoding is added to the
  embedding to give it order.
- The causal mask keeps a word from seeing what comes after it, so all
  positions are trained in parallel.
- Block = multi-head attention + feed-forward network, each with layer
  normalisation and a residual connection. The output has the input's size,
  and blocks are stacked.
- Parameters grow with `12d²`; large models are this block scaled up
  hundreds of times and stacked.
