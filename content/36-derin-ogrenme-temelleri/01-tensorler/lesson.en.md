# Tensors

In PyTorch everything is a **tensor**: the input image, the labels, the
model's weights, the loss. A tensor is a multi-dimensional array of numbers,
very much like a NumPy array. It has two differences: a tensor can carry
derivative information (in the Automatic Differentiation section) and it can
also live on a graphics card (GPU). In this section we learn to build a
tensor, read its shape and type, and change its shape.

## Building a tensor

The easiest way is to build it from a Python list:

```python
import torch

a = torch.tensor([1, 2, 3])
b = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print(a, a.dtype, a.shape)
print(b.dtype, b.shape, b.ndim)
print(b[1, 2], b[1, 2].item())
```

```text
tensor([1, 2, 3]) torch.int64 torch.Size([3])
torch.float32 torch.Size([2, 3]) 2
tensor(6.) 6.0
```

- `shape` is the number of elements in each dimension: `b` has 2 rows and
  3 columns. `ndim` is the number of dimensions.
- A tensor built from integers is `int64`; one built from decimals is
  `float32`. Neural network weights are `float32`.
- `b[1, 2]` is a one-element tensor; `.item()` gives the Python number
  inside it.

The names of the dimensions: a single number is a **scalar** (0
dimensions), a list of numbers a **vector** (1 dimension), a table a
**matrix** (2 dimensions). Beyond that it is simply called a "tensor".

## Ready-made constructors

We rarely type a tensor by hand; we build it in a given shape with zeros,
ones, a sequence or random numbers:

```python
print(torch.zeros(2, 3))
print(torch.ones(2, dtype=torch.int64))
print(torch.arange(0, 10, 3))
print(torch.linspace(0, 1, 5))
torch.manual_seed(0)
print(torch.rand(2, 2).shape, torch.randn(3).shape)
```

```text
tensor([[0., 0., 0.],
        [0., 0., 0.]])
tensor([1, 1])
tensor([0, 3, 6, 9])
tensor([0.0000, 0.2500, 0.5000, 0.7500, 1.0000])
torch.Size([2, 2]) torch.Size([3])
```

- `arange(start, end, step)` does not include the end; `linspace` puts 5
  evenly spaced numbers between the start and the end.
- `rand` gives uniform random numbers between 0 and 1, `randn` random numbers
  with mean 0 and standard deviation 1. `torch.manual_seed(0)` fixes the
  random generator: the same seed gives the same numbers.

## Going back and forth with NumPy

Data often arrives as a NumPy array (scikit-learn, pandas). There are two
ways, and their difference matters:

```python
import numpy as np

arr = np.array([1.0, 2.0, 3.0])
copied = torch.tensor(arr)
shared = torch.from_numpy(arr)
arr[0] = 100.0
print(copied.tolist(), shared.tolist())
print(copied.dtype, shared.numpy().dtype)
```

```text
[1.0, 2.0, 3.0] [100.0, 2.0, 3.0]
torch.float64 float64
```

- `torch.tensor(arr)` **copies** the data; changing the array does not
  affect the copy.
- `torch.from_numpy(arr)` **shares** the same memory: a change in the array
  shows in the tensor too. Good for avoiding a copy of large data, but easy
  to change without noticing.
- NumPy's decimal type is `float64`; the tensor becomes `float64` too.
  `.numpy()` turns a tensor back into a NumPy array.

## Converting the type (dtype)

If we give `float64` data to a layer with `float32` weights, PyTorch raises
an error:

```python
layer = torch.nn.Linear(3, 1)
x = torch.from_numpy(np.ones((2, 3)))
try:
    layer(x)
except RuntimeError as error:
    print(error)
print(layer(x.float()).shape, x.float().dtype)
```

```text
mat1 and mat2 must have the same dtype, but got Double and Float
torch.Size([2, 1]) torch.float32
```

The error message says the types of the two matrices (`mat1` the input,
`mat2` the weights) are not the same: `Double` is the name of `float64`,
`Float` of `float32`. `.float()` converts a tensor to `float32`, `.long()`
to `int64`; `x.to(torch.float32)` is the long form of the same thing. The
rule: **inputs are `float32`, class labels are `int64`.**

## Indexing and slicing

Selecting rows, columns and slices works as in NumPy:

```python
m = torch.arange(12).reshape(3, 4)
print(m)
print(m[0], m[:, 1].tolist())
print(m[1:, 2:].tolist())
print(m[m > 8].tolist())
```

```text
tensor([[ 0,  1,  2,  3],
        [ 4,  5,  6,  7],
        [ 8,  9, 10, 11]])
tensor([0, 1, 2, 3]) [1, 5, 9]
[[6, 7], [10, 11]]
[9, 10, 11]
```

- `m[0]` is the first row, `m[:, 1]` the second column (`:` means "all of
  this dimension").
- `m[1:, 2:]` is everything from the second row and the third column on.
- `m[m > 8]` gives the elements that meet the condition (selecting with a
  mask).

## Changing the shape

The most common job in deep learning is changing a tensor's shape: turning
an image into a flat vector, adding a "batch" dimension in front.

```python
t = torch.arange(6)
print(t.reshape(2, 3).tolist())
print(t.reshape(3, -1).shape)
v = t.reshape(1, 6)
print(v.shape, v.squeeze().shape)
print(t.unsqueeze(0).shape, t.unsqueeze(1).shape)
```

```text
[[0, 1, 2], [3, 4, 5]]
torch.Size([3, 2])
torch.Size([1, 6]) torch.Size([6])
torch.Size([1, 6]) torch.Size([6, 1])
```

- `reshape` changes the shape as long as the number of elements stays the
  same (6 = 2 × 3). `-1` means "work out this dimension yourself".
- `unsqueeze(0)` adds a dimension of length 1 in front, `squeeze()` drops
  the dimensions of length 1.

## Image tensors

The `dl_data` module in this track's exercises makes simple shape images
with a fixed seed (circle, square, triangle). The images are in the order
PyTorch expects: **(count, channels, height, width)**.

```python
from dl_data import make_shapes

images, labels = make_shapes(100, size=16)
x = torch.from_numpy(images)
print(x.shape, x.dtype, labels[:6].tolist())
flat = x.flatten(start_dim=1)
print(flat.shape, x[0].shape, x[0, 0].shape)
```

```text
torch.Size([100, 1, 16, 16]) torch.float32 [2, 1, 2, 2, 1, 2]
torch.Size([100, 256]) torch.Size([1, 16, 16]) torch.Size([16, 16])
```

<figure class="fig">
  <div class="flow">
    <span class="node">100 images</span><span class="arrow">→</span>
    <span class="node">1 channel<br><small>grey</small></span><span class="arrow">→</span>
    <span class="node">16 rows</span><span class="arrow">→</span>
    <span class="node acc">16 columns</span>
  </div>
  <figcaption>(100, 1, 16, 16): the first dimension is the image number, the second the channel (1 for a grey image, 3 for a colour one), the last two the pixels.</figcaption>
</figure>

`flatten(start_dim=1)` keeps the first dimension (the image number) and turns
the rest into a flat vector: each image becomes 1 × 16 × 16 = 256 numbers.
The `nn.Linear(64, ...)` layer in the introduction also took the 8 × 8
digits flattened like this.

## Summary

- A tensor is PyTorch's multi-dimensional array; read it with `shape`,
  `dtype`, `ndim`.
- `torch.tensor` copies, `torch.from_numpy` shares the memory.
- Inputs are `float32` (`.float()`), class labels `int64` (`.long()`).
- `reshape`, `flatten`, `unsqueeze`, `squeeze` change the shape; the number
  of elements stays the same.
- Images are in (count, channels, height, width) order.
