A short version of everything in the lesson. Come back here when you get stuck on a question.

## Definitions

| Concept | Formula |
|---|---|
| partial derivative | $\dfrac{\partial f}{\partial x}$: the other variables fixed |
| gradient | $\nabla f = \left(\dfrac{\partial f}{\partial x}, \dfrac{\partial f}{\partial y}, \ldots\right)$ |
| directional derivative | $D_{\mathbf{u}} f = \nabla f \cdot \mathbf{u}$, $\lVert \mathbf{u} \rVert = 1$ |
| fastest increase | along $\nabla f$, at rate $\lVert \nabla f \rVert$ |
| fastest decrease | along $-\nabla f$ |

## Taking partial derivatives

| Expression | $\partial / \partial x$ | $\partial / \partial y$ |
|---|---|---|
| $x^2 y$ | $2xy$ | $x^2$ |
| $3y$ | $0$ | $3$ |
| $e^{xy}$ | $y e^{xy}$ | $x e^{xy}$ |
| $x^2 + y^2$ | $2x$ | $2y$ |

## The geometry of the gradient

| Property | Explanation |
|---|---|
| direction | steepest ascent |
| level curve | the gradient is perpendicular to it |
| $\theta = 90°$ | no change in that direction |

## Points where the gradient is zero

| Kind | Example (at $(0, 0)$) |
|---|---|
| minimum | $x^2 + y^2$ |
| maximum | $-x^2 - y^2$ |
| saddle | $x^2 - y^2$ |

## Machine learning

| Concept | Formula |
|---|---|
| linear model, one example | $\dfrac{\partial L}{\partial w_j} = 2(\hat{y} - y) x_j$ |
| vector form | $\nabla_{\mathbf{w}} L = 2(\hat{y} - y) \mathbf{x}$ |
| gradient descent | $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$ |

## Practical tips

- In a partial derivative the other variables stay as factors; on their own their derivative is $0$.
- For a directional derivative, make the direction vector a unit vector first.
- For mixed derivatives the order does not matter: $f_{xy} = f_{yx}$.
