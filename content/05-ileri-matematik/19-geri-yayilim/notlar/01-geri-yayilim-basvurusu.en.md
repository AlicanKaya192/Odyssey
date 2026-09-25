A short version of everything in the lesson. Come back here when you get stuck on a question.

## Two passes

| Pass | Direction | Job |
|---|---|---|
| forward | input → output | compute and store the values |
| backward | output → input | start from $\frac{\partial L}{\partial L} = 1$; upstream gradient × local derivative |

## Gates (incoming gradient g)

| Node | Sent to the inputs |
|---|---|
| $a + b$ | $g$, $g$ |
| $a - b$ | $g$, $-g$ |
| $a \cdot b$ | $g b$, $g a$ |
| $\max(a, b)$ | $g$ to the larger, $0$ to the smaller |
| $\mathrm{ReLU}(z)$ | $g$ if $z > 0$, otherwise $0$ |
| $\sigma(z)$ | $g \, \sigma(1 - \sigma)$ |
| $e^z$ | $g \, e^z$ |
| branching | the sum of what comes in |

## One layer

$\mathbf{z} = W\mathbf{x} + \mathbf{b}$, $\mathbf{a} = \phi(\mathbf{z})$

| Derivative | Formula |
|---|---|
| $\frac{\partial L}{\partial \mathbf{z}}$ | $\frac{\partial L}{\partial \mathbf{a}} \odot \phi'(\mathbf{z})$ |
| $\frac{\partial L}{\partial W}$ | $\frac{\partial L}{\partial \mathbf{z}} \, \mathbf{x}^\mathsf{T}$ |
| $\frac{\partial L}{\partial \mathbf{b}}$ | $\frac{\partial L}{\partial \mathbf{z}}$ |
| $\frac{\partial L}{\partial \mathbf{x}}$ | $W^\mathsf{T} \frac{\partial L}{\partial \mathbf{z}}$ |

## Common losses

| Loss | $\frac{\partial L}{\partial \hat{y}}$ |
|---|---|
| $\frac{1}{2}(\hat{y} - y)^2$ | $\hat{y} - y$ |
| $(\hat{y} - y)^2$ | $2(\hat{y} - y)$ |

## Cost

| Topic | Explanation |
|---|---|
| time | one backward pass ≈ a few forward passes |
| memory | the forward pass's intermediate values are stored |
| numerical derivatives | as many forward passes as weights |

## Deep networks

| Problem | Cause | Remedy |
|---|---|---|
| vanishing gradients | factors $< 1$ (sigmoid $\le 0.25$) | ReLU, residual connections, good initialisation |
| exploding gradients | factors $> 1$ | clipping, good initialisation, normalisation |
