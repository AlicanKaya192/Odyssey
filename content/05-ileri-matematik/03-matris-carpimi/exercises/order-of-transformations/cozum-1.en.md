**What is asked?** The same two transformations in two different orders. We will see whether the results differ.

**Idea:** Turn each matrix into a rule, then apply the rules to the vector in order:

- $R$: $(x, y) \to (-y,\ x)$ (a quarter turn to the left)
- $S$: $(x, y) \to (x,\ -y)$ (mirror in the $x$-axis)

**Order 1 — Step 1: rotate.** $(1, 3) \to (-3,\ 1)$.

**Order 1 — Step 2: reflect.** The sign of $y$ flips: $(-3, 1) \to (-3,\ -1)$.

**Order 2 — Step 1: reflect.** $(1, 3) \to (1,\ -3)$.

**Order 2 — Step 2: rotate.** For $(x, y) = (1, -3)$, $(-y, x) = (3,\ 1)$.

**Reading the result:** The two results are exact opposites: $(-3, -1)$ and $(3, 1)$. The same two moves, merely swapped, sent the vector in opposite directions. This is the geometric picture of matrix multiplication not being commutative.

**Check:** Rotations and reflections preserve length. $\|(1, 3)\| = \sqrt{10}$, and both results have length $\sqrt{9 + 1} = \sqrt{10}$. ✓

**Answer:** Order 1 gives $(-3, -1)$; order 2 gives $(3, 1)$.
