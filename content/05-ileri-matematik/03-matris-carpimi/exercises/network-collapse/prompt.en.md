A small two-layer network without activation functions takes a 2-component input first to 3 neurons, then to a single output:

$$
W_1 = \begin{bmatrix} 1 & 2 \\ 0 & 1 \\ 1 & -1 \end{bmatrix}
$$

$$
W_2 = \begin{bmatrix} 1 & 0 & 2 \end{bmatrix}
$$

The output is $y = W_2(W_1\mathbf{x})$.

1. Find the two entries of the single matrix $W = W_2 W_1$ that replaces both layers.
2. What is the output $y$ for the input $\mathbf{x} = (2, 1)$?
