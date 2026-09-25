A layer: $\mathbf{z} = W\mathbf{x}$, $\mathbf{a} = \mathrm{ReLU}(\mathbf{z})$, loss $L = \frac{1}{2}\lVert \mathbf{a} - \mathbf{y} \rVert^2$.

$$
W = \begin{bmatrix} 1 & 2 \\ 3 & -1 \end{bmatrix}, \quad \mathbf{x} = (1, 1), \quad \mathbf{y} = (1, 1)
$$

1. What is $\dfrac{\partial L}{\partial x_1}$?
2. What is $\dfrac{\partial L}{\partial x_2}$?
3. What is $\dfrac{\partial L}{\partial W_{12}}$?
