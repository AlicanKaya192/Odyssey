**Idea:** Write the trace as a single sum by looking at which pairs of entries are multiplied and added. Inside $\operatorname{tr}(AB)$, each entry of $A$ is multiplied once by the entry of $B$ in the "mirror" position:

$$
\operatorname{tr}(AB) = \sum_{i} \sum_{k} a_{ik}\, b_{ki}
$$

**Step 1 — Pair up the entries.** The partner of $a_{ik}$ is $b_{ki}$ (row and column numbers swapped). $A$ is $2 \times 3$, so there are 6 pairs:

$$
\begin{aligned}
a_{11} b_{11} &= 1 \cdot 3 = 3 \\
a_{12} b_{21} &= 0 \cdot 2 = 0 \\
a_{13} b_{31} &= 2 \cdot 1 = 2 \\
a_{21} b_{12} &= -1 \cdot 1 = -1 \\
a_{22} b_{22} &= 3 \cdot 1 = 3 \\
a_{23} b_{32} &= 1 \cdot 0 = 0
\end{aligned}
$$

**Step 2 — Add.**

$$
3 + 0 + 2 - 1 + 3 + 0 = 7
$$

**Step 3 — The same sum for $BA$.** $\operatorname{tr}(BA) = \sum_k \sum_i b_{ki}\, a_{ik}$: the pairs multiplied are **exactly the same** six pairs, only added in a different order. So $\operatorname{tr}(BA) = 7$.

**Why is it useful?** This method gives both traces at once and shows why the rule $\operatorname{tr}(AB) = \operatorname{tr}(BA)$ holds. You will meet the rule again in the eigenvalues section, where the trace turns out to be the sum of the eigenvalues.

**Answer:** $7$ and $7$.
