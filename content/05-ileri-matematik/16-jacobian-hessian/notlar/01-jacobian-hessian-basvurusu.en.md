A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Definition | Size |
|---|---|---|
| gradient | $\nabla f$, partial derivatives of one output | $n$ |
| Jacobian | $J_{ij} = \dfrac{\partial F_i}{\partial x_j}$ | $m \times n$ |
| Hessian | $H_{ij} = \dfrac{\partial^2 f}{\partial x_i \, \partial x_j}$ | $n \times n$, symmetric |

## Approximations

| Order | Formula |
|---|---|
| first (Jacobian) | $F(\mathbf{p} + \mathbf{h}) \approx F(\mathbf{p}) + J \mathbf{h}$ |
| second (Hessian) | $f(\mathbf{p} + \mathbf{h}) \approx f(\mathbf{p}) + \nabla f \cdot \mathbf{h} + \tfrac{1}{2} \mathbf{h}^\mathsf{T} H \mathbf{h}$ |

## The chain rule

| Situation | Formula |
|---|---|
| $z = f(x(t), y(t))$ | $\dfrac{dz}{dt} = f_x \, x' + f_y \, y'$ |
| composition | $J_{g \circ f} = J_g \, J_f$ |
| linear layer, backwards | $\dfrac{\partial L}{\partial \mathbf{x}} = W^\mathsf{T} \dfrac{\partial L}{\partial \mathbf{z}}$ |
| with respect to the weights | $\dfrac{\partial L}{\partial W} = \dfrac{\partial L}{\partial \mathbf{z}} \, \mathbf{x}^\mathsf{T}$ |

## Critical point (zero gradient)

| Hessian | Point |
|---|---|
| eigenvalues all $> 0$ | minimum |
| eigenvalues all $< 0$ | maximum |
| mixed signs | saddle |
| two variables: $\det H > 0$, $f_{xx} > 0$ | minimum |
| two variables: $\det H > 0$, $f_{xx} < 0$ | maximum |
| two variables: $\det H < 0$ | saddle |

## Ready-made Jacobians

| Function | Jacobian |
|---|---|
| $W\mathbf{x} + \mathbf{b}$ | $W$ |
| element-wise $\sigma(\mathbf{z})$ | diagonal, $\sigma'(z_i)$ |
| ReLU | diagonal, $0$ or $1$ |

## Machine learning

- A stable learning rate: $\eta < \dfrac{2}{\lambda_{\max}}$ (roughly).
- Newton: $\Delta = -H^{-1} \nabla f$.
