# Embedding Layers and Preparing Sequences

The networks so far took fixed-size input: a table row with 6 features or a
16×16 image. Text, audio and sensor recordings are **sequences**: their items
come in order and every example has a different length. The first half of
this module is networks that work on sequences; this section is the first
step they all share: **turning a word into a number and a number into a
vector**, and fitting sequences of different lengths into one tensor.

The idea of an embedding was covered in the Embeddings and Language Models
module: every word is represented by a short vector, words with similar
meanings land close to each other, and the vectors are learned by training.
There we picked the rows of a matrix ourselves with NumPy. In PyTorch the same
job is a single layer: `nn.Embedding`.

<figure class="fig">
<div class="flow">
<span class="node">text</span><span class="arrow">→</span>
<span class="node">ids</span><span class="arrow">→</span>
<span class="node">padding</span><span class="arrow">→</span>
<span class="node">nn.Embedding</span><span class="arrow">→</span>
<span class="node acc">(B, T, D)</span>
</div>
<figcaption>The steps a sequence goes through before it enters the network. B is the batch size, T the length of the longest sequence, D the embedding size.</figcaption>
</figure>

## From word to id

A network does not read words, it reads numbers. First we build a
**vocabulary**: every word gets an integer **id**. We reserve the first two
ids for two special tokens: `<pad>` (padding, 0) and `<unk>` (unknown word,
1). We will see shortly why they are needed.

```python
from dl_data import TEXT

sentences = [s.split() for s in TEXT.split(".") if s.strip()]
words = sorted({w for s in sentences for w in s})
vocab = ["<pad>", "<unk>"] + words
index = {w: i for i, w in enumerate(vocab)}


def encode(sentence):
    return [index.get(w, 1) for w in sentence]


print(len(sentences), len(vocab))
print(sentences[0])
print(encode(sentences[0]))
```

```text
10 26
['the', 'cat', 'sat', 'on', 'the', 'mat']
[21, 5, 17, 14, 21, 13]
```

- The text has 10 sentences; with the two special tokens the
  vocabulary has 26 words.
- `index.get(w, 1)`: a word not in the vocabulary gets the id of `<unk>`. A
  word never seen in training then does not stop the program.
- "the" appears twice and gets the same id both times: the id depends on the
  word itself, not on its position.

## `nn.Embedding`: from id to vector

`nn.Embedding(vocab_size, D)` holds a weight matrix of size `(vocab_size,
D)`. When id `i` comes in, it returns row `i` of the matrix. These rows are
ordinary parameters: they get derivatives in backpropagation and change with
training.

```python
import torch
from torch import nn

torch.manual_seed(0)
emb = nn.Embedding(len(vocab), 8)
ids = torch.tensor(encode(sentences[0]))
vectors = emb(ids)
print(ids.shape, ids.dtype)
print(vectors.shape, vectors.dtype)
print(emb.weight.shape, emb.weight.numel())
print(torch.equal(vectors, emb.weight[ids]))
```

```text
torch.Size([6]) torch.int64
torch.Size([6, 8]) torch.float32
torch.Size([26, 8]) 208
True
```

- The input must be **integers** (`int64`); the output is `float32`. Give
  the layer a floating point tensor and it raises an error.
- The shape rule: `D` is added to the end of the input's shape. 6 ids →
  `(6, 8)`. With a batch, `(B, T)` → `(B, T, 8)`.
- The parameter count is `vocab_size × D` = 208. As the
  vocabulary grows, the embedding is often the biggest layer of the model.
- The last line shows the layer's secret: `emb(ids)` and `emb.weight[ids]`
  are exactly the same. An embedding layer is a **row lookup**.

## Why a lookup and not a multiplication?

Turning the id into a one-hot vector and multiplying it with the weight
matrix gives the same result: the one-hot vector has a single 1, and the
product picks that row.

```python
one_hot = nn.functional.one_hot(ids, num_classes=len(vocab)).float()
print(one_hot.shape, one_hot.sum(dim=1).tolist())
print(torch.allclose(one_hot @ emb.weight, vectors))
```

```text
torch.Size([6, 26]) [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
True
```

The result is the same but the road is expensive: for every word we build a
vector of 26 numbers and do 26 × 8
multiplications. With a vocabulary of 50,000 words the difference is huge.
`nn.Embedding` takes the row directly.

## Different lengths: padding

A batch is one tensor and every row of a tensor must have the same length.
Sentences, though, have 5, 6, 9 words. The solution is **padding**: the id
of `<pad>` (0) is added to the end of the short sequences until all of them
are as long as the longest. `pad_sequence` does this.

```python
from torch.nn.utils.rnn import pad_sequence

batch = [torch.tensor(encode(s)) for s in sentences[:3]]
padded = pad_sequence(batch, batch_first=True, padding_value=0)
print([len(b) for b in batch])
print(padded.shape)
print(padded[2].tolist())
```

```text
[6, 6, 5]
torch.Size([3, 6])
[21, 5, 18, 21, 7, 0]
```

- `batch_first=True` makes the shape `(B, T)`. Without it the default is
  `(T, B)`: time first. We will meet this difference again with the LSTM in
  the next section.
- The third sentence has 5 words; one `0` was added to its end.

## Keeping track of padding: `padding_idx` and the mask

Padding is a trick; we do not want the network to learn it like a real word.
There are two tools:

- `nn.Embedding(..., padding_idx=0)`: the vector of id 0 starts at **zero**
  and never gets a derivative, so it stays zero during training.
- A **mask**: a boolean tensor saying which positions are real and which are
  padding, `padded != 0`. It is used to leave the padding out of an
  operation such as a mean, a sum or attention.

```python
torch.manual_seed(0)
emb = nn.Embedding(len(vocab), 8, padding_idx=0)
out = emb(padded)
mask = padded != 0
lengths = mask.sum(dim=1)
print(out.shape, mask.dtype, lengths.tolist())
print(out[~mask].abs().sum().item())

mean_all = out.mean(dim=1)
mean_real = (out * mask.unsqueeze(-1)).sum(dim=1) / lengths.unsqueeze(-1)
print(torch.allclose(mean_all[0], mean_real[0]))
print(torch.allclose(mean_all[2], mean_real[2]))
```

```text
torch.Size([3, 6, 8]) torch.bool [6, 6, 5]
0.0
True
False
```

- The sum of all numbers at the padding positions is 0: `padding_idx`
  works.
- But a zero vector still **enters** the mean. The first sentence has no
  padding and the two means agree (`True`). The third sentence has one pad:
  the plain `mean` divides by 6, the real length is 5, and the result
  differs (`False`). For a padded sequence, take the mean with the mask.
- `mask.unsqueeze(-1)` turns the mask from `(B, T)` into `(B, T, 1)` so that
  it can broadcast with `(B, T, 8)` (broadcasting is in the Deep Learning
  Fundamentals module).

Let us check that the padding really gets no derivative. The derivative of
the sum of the output with respect to a word's row is, in every column, the
number of times that word appears:

```python
out.sum().backward()
grad = emb.weight.grad
print(grad[0].abs().sum().item())
print(grad[index["the"]].sum().item())
```

```text
0.0
48.0
```

- The padding row (`0`) got a zero derivative: however much padding there
  is, this row does not change.
- "the" appears twice in each of three sentences, 6 times in total; each of
  the 8 columns gets a derivative of 6: 6 × 8 = 48.

## Batches with a DataLoader

By default a `DataLoader` (the Dataset and DataLoader section of the Deep
Learning Fundamentals module) stacks the examples on top of each other; with
sequences of different lengths this fails. We give it our own **collate
function** (`collate_fn`): it pads the examples that arrive as a list, turns
them into a tensor, and returns the real lengths alongside.

```python
from torch.utils.data import DataLoader


def collate(items):
    seqs = [torch.tensor(encode(s)) for s in items]
    lengths = torch.tensor([len(s) for s in seqs])
    return pad_sequence(seqs, batch_first=True), lengths


loader = DataLoader(sentences, batch_size=4, collate_fn=collate)
for x, lengths in loader:
    print(tuple(x.shape), lengths.tolist())
```

```text
(4, 9) [6, 6, 5, 9]
(4, 9) [6, 3, 9, 9]
(2, 9) [7, 9]
```

- The second dimension of each batch is the longest sentence of **that**
  batch; it does not have to be the same across batches.
- Keeping the lengths is not wasted: in the next section we use them to let
  the LSTM skip the padding.

## Summary

- The road to a prepared sequence: text → ids with a vocabulary → padding →
  embedding → `(B, T, D)`.
- `nn.Embedding` is a row lookup table; the same result as a one-hot
  product, much cheaper. The input is `int64`.
- `<pad>` is for padding, `<unk>` for unknown words. `padding_idx` keeps the
  padding vector at zero and without derivatives.
- A zero vector still enters a mean: on padded sequences take sums and
  means with the mask.
- For examples of different lengths give the `DataLoader` a `collate_fn` and
  return the lengths too.
