In the column view, $X\mathbf{w}$ is every feature column multiplied by its own weight and added up. Each column gives **that feature's contribution to the price of every house** in one go:

**The area's share:**

$$
100 \begin{bmatrix} 1.2 \\ 0.8 \\ 1.5 \end{bmatrix} = \begin{bmatrix} 120 \\ 80 \\ 150 \end{bmatrix}
$$

**The rooms' share:**

$$
20 \begin{bmatrix} 3 \\ 2 \\ 4 \end{bmatrix} = \begin{bmatrix} 60 \\ 40 \\ 80 \end{bmatrix}
$$

**The age's share:**

$$
-2 \begin{bmatrix} 10 \\ 25 \\ 5 \end{bmatrix} = \begin{bmatrix} -20 \\ -50 \\ -10 \end{bmatrix}
$$

**Add them all and $b = 10$:**

$$
\hat{\mathbf{y}} = \begin{bmatrix} 120 + 60 - 20 + 10 \\ 80 + 40 - 50 + 10 \\ 150 + 80 - 10 + 10 \end{bmatrix} = \begin{bmatrix} 170 \\ 80 \\ 230 \end{bmatrix}
$$

The benefit of this view: the reason house 2 comes out cheap is visible at once, its age contributes $-50$. Explaining a model's prediction by splitting it into features rests on this idea.

**Answer: $170$, $80$, $230$**
