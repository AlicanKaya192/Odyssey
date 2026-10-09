The essence of the kernel trick is an equality: some functions give **the
same result** as moving the points into a larger space and taking the inner
product there. For two-dimensional points, the second-degree kernel
`(a·b + 1)²` equals the inner product in a six-dimensional widening:

```python
import numpy as np


def phi(v):
    x1, x2 = v
    r = np.sqrt(2)
    return np.array([1, r * x1, r * x2, x1 * x1, x2 * x2, r * x1 * x2])


def poly_kernel(a, b):
    return (a @ b + 1) ** 2


a = np.array([1.0, 2.0])
b = np.array([3.0, -1.0])
print(round(phi(a) @ phi(b), 6), round(poly_kernel(a, b), 6))
print(len(phi(a)))
```

```text
0.641 0.976
0.939
```

Both ways give the same number: without building the six-dimensional vectors,
through the two-dimensional inner product. As the dimension grows, the
difference becomes huge: on data with 100 features a second-degree widening
needs more than 5,000 dimensions, while the kernel is still a single inner
product and a square. The RBF kernel `exp(−γ ‖a − b‖²)` corresponds to an
infinite-dimensional widening; building it explicitly is impossible, computing
it with the kernel is easy.

The price: a kernel SVM looks at the kernel value between all pairs of points;
training time grows roughly quadratically with the number of samples. Beyond
tens of thousands of rows, a linear SVM or other methods are preferred.
