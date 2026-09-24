**What is asked?** The traces of two products. The trace consists only of the diagonal entries, so there is no need to compute the whole products.

**Idea:** $c_{ii}$ = row $i$ of the left matrix · column $i$ of the right matrix. For each trace we compute only these entries.

**Step 1 — Sizes.** $AB$: $(2 \times 3)(3 \times 2) = 2 \times 2$, with 2 diagonal entries. $BA$: $(3 \times 2)(2 \times 3) = 3 \times 3$, with 3 diagonal entries.

**Step 2 — The diagonal of $AB$.** The rows of $A$ are $(1, 0, 2)$ and $(-1, 3, 1)$; the columns of $B$ are $(3, 2, 1)$ and $(1, 1, 0)$.

$$
\begin{aligned}
(AB)_{11} &= 1 \cdot 3 + 0 \cdot 2 + 2 \cdot 1 = 5 \\
(AB)_{22} &= -1 \cdot 1 + 3 \cdot 1 + 1 \cdot 0 = 2
\end{aligned}
$$

$$
\operatorname{tr}(AB) = 5 + 2 = 7
$$

**Step 3 — The diagonal of $BA$.** The rows of $B$ are $(3, 1)$, $(2, 1)$, $(1, 0)$; the columns of $A$ are $(1, -1)$, $(0, 3)$, $(2, 1)$.

$$
\begin{aligned}
(BA)_{11} &= 3 \cdot 1 + 1 \cdot (-1) = 2 \\
(BA)_{22} &= 2 \cdot 0 + 1 \cdot 3 = 3 \\
(BA)_{33} &= 1 \cdot 2 + 0 \cdot 1 = 2
\end{aligned}
$$

$$
\operatorname{tr}(BA) = 2 + 3 + 2 = 7
$$

**Reading the result:** $AB$ and $BA$ have different sizes and are completely different matrices, yet their traces agree. This is no coincidence: always $\operatorname{tr}(AB) = \operatorname{tr}(BA)$. The second method shows why.

**Answer:** $\operatorname{tr}(AB) = 7$, $\operatorname{tr}(BA) = 7$.
