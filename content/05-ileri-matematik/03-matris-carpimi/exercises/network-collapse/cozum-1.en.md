**What is asked?** To show that two linear layers collapse into one matrix: first we find that matrix, then we compute the output for one input.

**Idea:** Associativity: $W_2(W_1\mathbf{x}) = (W_2 W_1)\mathbf{x}$. Without a non-linear operation in between, two layers do the same job as a single layer given by their product.

**Step 1 — Size.** $(1 \times 3)(3 \times 2) = 1 \times 2$: $W$ is a single row with two numbers.

**Step 2 — Entry 1 of $W$.** The row of $W_2$, $(1, 0, 2)$, with column 1 of $W_1$, $(1, 0, 1)$:

$$
w_1 = 1 \cdot 1 + 0 \cdot 0 + 2 \cdot 1 = 3
$$

**Step 3 — Entry 2 of $W$.** The same row with column 2, $(2, 1, -1)$:

$$
\begin{aligned}
w_2 &= 1 \cdot 2 + 0 \cdot 1 + 2 \cdot (-1) \\
&= 2 + 0 - 2 = 0
\end{aligned}
$$

$$
W = \begin{bmatrix} 3 & 0 \end{bmatrix}
$$

**Step 4 — The output.** Apply the single matrix to the input:

$$
y = W\mathbf{x} = 3 \cdot 2 + 0 \cdot 1 = 6
$$

**Reading the result:** Entry 2 of $W$ is $0$: this network **ignores** the second input component entirely. In the hidden layer its effect passes through one neuron with a plus sign and another with a minus sign, and in the end they cancel. Despite the three hidden neurons, the whole network is as simple as "three times the first input component".

**Answer:** $W = (3, 0)$, $y = 6$.
