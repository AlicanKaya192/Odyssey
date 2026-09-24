**Idea:** First run the network for real (layer by layer), then find $W$ with a different view: a $1 \times 3$ row times a matrix is a weighted sum of that matrix's **rows**.

**Step 1 — Layer 1.** $W_1\mathbf{x}$, one dot product per neuron:

$$
W_1 \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \cdot 2 + 2 \cdot 1 \\ 0 \cdot 2 + 1 \cdot 1 \\ 1 \cdot 2 - 1 \cdot 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 1 \\ 1 \end{bmatrix}
$$

**Step 2 — Layer 2.** The hidden output with $W_2$:

$$
y = 1 \cdot 4 + 0 \cdot 1 + 2 \cdot 1 = 6
$$

**Step 3 — Build $W$ from the rows.** Since $W_2 = (1, 0, 2)$, $W_2 W_1$ is 1 times row 1 of $W_1$, plus 0 times row 2, plus 2 times row 3:

$$
\begin{aligned}
W &= 1 \cdot (1, 2) + 0 \cdot (0, 1) + 2 \cdot (1, -1) \\
&= (1, 2) + (2, -2) \\
&= (3, 0)
\end{aligned}
$$

**Check:** With the single matrix the output is $3 \cdot 2 + 0 \cdot 1 = 6$, the same as layer by layer. ✓

**Why is it useful?** With a million inputs, the layer-by-layer route needs 6 + 3 = 9 multiplications per input, the single matrix only 2. But there is a price: this network can never learn anything beyond one matrix. That is why a curved function such as ReLU goes between the layers.

**Answer:** $W = (3, 0)$, $y = 6$.
