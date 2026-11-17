# Tensor Operations and Broadcasting

What happens inside a neural network is just a few kinds of operations on
tensors: element-wise arithmetic, matrix multiplication, **reductions** such
as sums and means, and **broadcasting**, which lets tensors of different
shapes work together. In this section we look at these four and at the end
rewrite the `nn.Linear` layer as a one-line matrix product.

## Element-wise operations

`+`, `-`, `*`, `/`, `**` work between matching elements of two tensors of
the same shape:

```python
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[10.0, 20.0], [30.0, 40.0]])
print((a + b).tolist())
print((a * b).tolist())
print((a ** 2).tolist(), torch.sqrt(a)[1, 1].item())
```

```text
[[11.0, 22.0], [33.0, 44.0]]
[[10.0, 40.0], [90.0, 160.0]]
[[1.0, 4.0], [9.0, 16.0]] 2.0
```

`a * b` is **not matrix multiplication**: it multiplies the elements in the
same place. Functions in `torch` such as `sqrt`, `exp`, `log` and `abs` are
also applied to each element separately.

## Matrix multiplication

Matrix multiplication is written with `@` (or `torch.matmul`). A matrix of
shape `(a, b)` can be multiplied by a matrix of shape `(b, c)`; the result is
`(a, c)`:

```python
x = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
w = torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
print(x.shape, w.shape, (x @ w).shape)
print((x @ w).tolist())
```

```text
torch.Size([2, 3]) torch.Size([3, 2]) torch.Size([2, 2])
[[4.0, 5.0], [10.0, 11.0]]
```

Each element of the result is the **dot product** of a row and a column: the
first row `[1, 2, 3]` with the first column `[1, 0, 1]` → `1 + 0 + 3 = 4`.
Most of a neural network's work is this product.

## Reductions and `dim`

`sum`, `mean` and `max` shrink a tensor. `dim` says along which dimension to
reduce:

```python
t = torch.tensor([[1.0, 5.0, 3.0], [4.0, 2.0, 6.0]])
print(t.sum().item(), t.sum(dim=0).tolist(), t.sum(dim=1).tolist())
print(t.mean(dim=1, keepdim=True).shape)
values, indices = t.max(dim=1)
print(values.tolist(), indices.tolist(), t.argmax(dim=1).tolist())
```

```text
21.0 [5.0, 7.0, 9.0] [9.0, 12.0]
torch.Size([2, 1])
[5.0, 6.0] [1, 2] [1, 2]
```

<figure class="fig">
  <div class="versus">
    <div><h5><code>dim=0</code></h5>Reduces down the rows: one result for each <b>column</b>. <code>(2, 3)</code> → <code>(3,)</code></div>
    <div><h5><code>dim=1</code></h5>Reduces across the columns: one result for each <b>row</b>. <code>(2, 3)</code> → <code>(2,)</code></div>
  </div>
  <figcaption>Read <code>dim</code> as "the dimension to remove": it does not survive in the result.</figcaption>
</figure>

- `keepdim=True` leaves the reduced dimension with length 1: `(2, 3)` →
  `(2, 1)`. Handy when the result goes back into an operation with the
  original tensor.
- `max(dim=1)` returns two things: the largest values and their positions.
  If you only need the position, use `argmax`.

## Broadcasting

Adding two tensors of different shapes is possible too. PyTorch
**broadcasts** the smaller one: it behaves as if copied along missing or
length-1 dimensions, without actually copying.

```python
m = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
print((m + torch.tensor([10.0, 100.0])).tolist())
col = torch.tensor([[1.0], [2.0], [3.0]])
row = torch.tensor([[10.0, 20.0, 30.0, 40.0]])
print(col.shape, row.shape, (col + row).shape)
try:
    m + torch.tensor([1.0, 2.0, 3.0])
except RuntimeError as error:
    print(str(error).replace(" at ", "\nat "))
```

```text
[[11.0, 102.0], [13.0, 104.0], [15.0, 106.0]]
torch.Size([3, 1]) torch.Size([1, 4]) torch.Size([3, 4])
The size of tensor a (2) must match the size of tensor b (3)
at non-singleton dimension 1
```

The rule is to compare the shapes **from the right**: in each dimension the
two lengths must be equal, or one of them must be 1 (or missing).

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>(3, 2) + (2,)</code></span><span>The 2 on the right equals 2; a missing dimension counts as 1 → <code>(3, 2)</code></span></div>
    <div class="anat-row"><span><code>(3, 1) + (1, 4)</code></span><span>The ones stretch → <code>(3, 4)</code></span></div>
    <div class="anat-row"><span><code>(3, 2) + (3,)</code></span><span>2 and 3 on the right do not match → error</span></div>
  </div>
  <figcaption>The broadcasting rule: align from the right, each dimension equal or 1.</figcaption>
</figure>

The error message names the mismatched dimension: 2 and 3 in dimension
number 1 (the columns). If you want to add one value per row, give the value
a column shape: `(3, 1)` instead of `(3,)`.

## In practice: scaling the columns

In the machine learning track, `StandardScaler` scaled each feature to mean
0 and standard deviation 1. With broadcasting it is one line:

```python
from dl_data import make_table

x_np, y_np = make_table(600)
x = torch.from_numpy(x_np)
scaled = (x - x.mean(dim=0)) / x.std(dim=0)
print(x.shape, x.mean(dim=0).shape)
print(scaled.mean(dim=0).abs().max().item() < 1e-5)
print(torch.allclose(scaled.std(dim=0), torch.ones(6)))
```

```text
torch.Size([600, 6]) torch.Size([6])
True
True
```

`x.mean(dim=0)` is the mean of each column, shape `(6,)`; when it is
subtracted from `x` of shape `(600, 6)` it is broadcast to every row. The
scaled data has a mean very close to zero and a standard deviation of 1.

## What does `nn.Linear` really do?

The introduction's `nn.Linear(64, 32)` layer is nothing more than a matrix
product plus a broadcast addition: `x @ W.T + b`.

```python
torch.manual_seed(0)
layer = torch.nn.Linear(6, 3)
by_hand = x @ layer.weight.T + layer.bias
print(layer.weight.shape, layer.bias.shape)
print(by_hand.shape, torch.allclose(layer(x), by_hand))
```

```text
torch.Size([3, 6]) torch.Size([3])
torch.Size([600, 3]) True
```

- The weight is stored as `(output, input)` = `(3, 6)`; that is why it is
  multiplied by its transpose (`W.T`, `(6, 3)`): `(600, 6) @ (6, 3)` →
  `(600, 3)`.
- The bias `b` has shape `(3,)` and is broadcast to each of the 600 rows.
- `torch.allclose` says two tensors are the same (apart from tiny rounding
  differences). The layer does exactly the computation we wrote.

## Summary

- `*` is element-wise, `@` is matrix multiplication. `(a, b) @ (b, c)` →
  `(a, c)`.
- `dim` is the dimension to reduce (it leaves the result); `keepdim=True`
  keeps it with length 1.
- Broadcasting: shapes align from the right, each dimension equal or 1.
- `nn.Linear` = `x @ W.T + b`.
