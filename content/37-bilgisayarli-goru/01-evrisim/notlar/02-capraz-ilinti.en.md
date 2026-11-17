In mathematics and signal processing courses, "convolution" first flips the
kernel in both directions, then multiplies and adds. `F.conv2d` does not
flip: what it does is **cross-correlation**. Let us see the difference in a
small example:

```python
import torch
import torch.nn.functional as F

x = torch.arange(16.0).reshape(1, 1, 4, 4)
k = torch.tensor([[1.0, 2.0], [3.0, 4.0]]).reshape(1, 1, 2, 2)
cross = F.conv2d(x, k)
flipped = torch.flip(k, dims=[2, 3])
true_conv = F.conv2d(x, flipped)
print(cross[0, 0].tolist())
print(true_conv[0, 0].tolist())
```

```text
[[34.0, 44.0, 54.0], [74.0, 84.0, 94.0], [114.0, 124.0, 134.0]]
[[16.0, 26.0, 36.0], [56.0, 66.0, 76.0], [96.0, 106.0, 116.0]]
```

- With the same kernel the two operations give different numbers.
- If you want true convolution, flipping the kernel with `torch.flip` and
  passing it to `F.conv2d` is enough.
- In a network the difference does not matter: the kernel is learned. If the
  network needs a flipped pattern, it simply learns the numbers already
  flipped.

When you take a ready-made edge kernel (such as Sobel) from a book and apply
it by hand, this difference can flip the sign of the result; testing it on an
example is a good habit.
