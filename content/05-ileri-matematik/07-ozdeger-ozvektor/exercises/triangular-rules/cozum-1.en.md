**What is asked?** Three facts about the eigenvalues without computing them one by one.

**Idea:** For a triangular matrix, $A - \lambda I$ is triangular too, and its determinant is the product of its diagonal. So $\det(A - \lambda I) = (2 - \lambda)(3 - \lambda)(-1 - \lambda)$, and the eigenvalues are simply the diagonal entries.

**Step 1 — The eigenvalues.** The diagonal: $2$, $3$, $-1$. The $1, 4, 5$ above the diagonal do not affect the eigenvalues.

**Step 2 — The sum.**

$$
2 + 3 + (-1) = 4
$$

Check: the trace is $2 + 3 - 1 = 4$ ✓ (the sum always equals the trace).

**Step 3 — The product.**

$$
2 \cdot 3 \cdot (-1) = -6
$$

Check: the determinant of a triangular matrix is also the product of its diagonal, $-6$ ✓.

**Step 4 — The eigenvalues of $A^2$.** The power rule: if $A\mathbf{v} = \lambda\mathbf{v}$ then $A^2\mathbf{v} = \lambda^2\mathbf{v}$. The squares:

$$
2^2 = 4, \qquad 3^2 = 9, \qquad (-1)^2 = 1
$$

The largest is $9$.

**Watch out:** Computing $A^2$ and looking at its diagonal also works (the square of a triangular matrix is triangular, with diagonal $4, 9, 1$), but the rule gives it in one line.

**Answer:** $4$, $-6$, $9$.
